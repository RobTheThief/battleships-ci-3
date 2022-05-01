import copy
import gspread
import os
import time
import math
from numpy import random
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ci-3-python')

class create_game_board:
    def __init__(self, size, ships, name = 'Computer'):
        self.size = size
        self.ships = ships
        self.name = name
        self.board_matrix = []
        self.board_matrix_obscured = []
        self.hit_count = 0
        self.current_history = []
        self.data_row = 0
        self.whos_turn = 'nobody'
        self.turn_count = 0
        self.round_count = 0

    def build_board(self):
        '''
        builds the board matrix according to size and saves it
        to the board object twice. The second is deep copied
        and used as a blank board for the opponent.
        '''
        for row in range( 0, self.size ):
            row_list = [' .' for cell in range( 0, self.size )]
            self.board_matrix.append(row_list)
        self.board_matrix_obscured = copy.deepcopy(self.board_matrix)

    def add_ships(self):
        '''
        adds ships to unique random coordinates according to ship number
        '''

        self.build_board()
        for _ in range(0, self.ships):
            done = False
            while not done:
                random_row = get_random(self.size)
                random_col = get_random(self.size)
                if self.board_matrix[random_row][random_col] != '<>':
                    self.board_matrix[random_row][random_col] = '<>'
                    done = True
        if self.name != 'Computer':            
            self.login_player()

    def recieve_shot(self, row, col):
        '''
            checks if given coordinates are a hit or miss and updates the board
        '''

        if self.board_matrix[row - 1][col - 1] == '<>':
            self.board_matrix[row - 1][col - 1] = ' #'
            self.board_matrix_obscured[row - 1][col - 1] = ' #'
            self.hit_count += 1
            return 'Hit'
        elif self.board_matrix[row - 1][col - 1] == ' .':
            self.board_matrix[row - 1][col - 1] = ' X'
            self.board_matrix_obscured[row - 1][col - 1] = ' X'
            return 'Miss'
        elif self.board_matrix[row - 1][col - 1] == ' X' or self.board_matrix[row - 1][col - 1] == ' #':
            return '**ALREADY FIRED ON THESE COORDINATES. TRY AGAIN'

    def find_player_row(self):
        """
            Finds which row the players data is on
            and saves the data and the row number to
            the board object. 
        """
        data = get_data()
        all_values = data[0]
        count = -1
        found = False
        for row in all_values:
            try:
                find = row.index(self.name)
                self.current_history = row
                count += 1
                self.data_row = count
                found = True
                break
            except ValueError:
                count += 1
        return found

    def add_new_player(self):
        """ 
            Creates new player in the sheet and saves the
            current_history to the board object
        """
        data = get_data()
        all_values = data[0]
        scores = data[1]
        pword = input('New player! Enter a password:\n')
        length = len(all_values)
       
        update_cell(f'A{length + 1}', self.name, scores) #Name
        update_cell(f'B{length + 1}', 0, scores) #Wins
        update_cell(f'C{length + 1}', 0, scores) #Losses
        update_cell(f'D{length + 1}', 0, scores) #Current Streak
        update_cell(f'E{length + 1}', 0, scores) #Best Streak
        update_cell(f'F{length + 1}', pword, scores) #Password

        data = get_data()
        all_values = data[0]
        self.current_history = all_values[length - 1]

    def login_player(self):
        """ 
            Checks if player has an account and logs them in.
            If no player found then redericted to create new player.
        """
        found = self.find_player_row()
        if not found:
            self.add_new_player()
        elif found:
            password_wrong = True
            while password_wrong:
                pword = input('Enter your password:\n')
                if pword == self.current_history[5]:
                    print('PREVIOUS SCORES: ','WINS', self.current_history[1], 'LOSSES', self.current_history[2])
                    print('CURRENT WIN STREAK', self.current_history[3], 'BEST STREAK', self.current_history[4])
                    password_wrong = False
                    break
                loading_delay('Password Incorrect. Resetting game..', 2)
                run_game()

    def update_player_scores(self, win, loss):
        """ 
            Updates the database for player for wins, losses, current streak,
            best streak.
        """
        self.find_player_row()
        scores = get_data()[1]

        win_update = int(self.current_history[1]) + int(win)
        update_cell(f'B{self.data_row + 1}', win_update, scores) #Wins

        loss_update = int(self.current_history[2]) + int(loss)
        update_cell(f'C{self.data_row + 1}', loss_update, scores) #Lossses

        if loss == 1:
            update_cell(f'D{self.data_row + 1}', 0, scores) #Current Streak reset to 0
        elif win == 1:
            streak_update = int(self.current_history[3]) + int(1)
            update_cell(f'D{self.data_row + 1}', streak_update, scores) #Current Streak increase
        all_values = get_data()[0]
        if int(all_values[self.data_row][3]) > int(self.current_history[4]):
            best_streak = int(all_values[self.data_row][3])
            update_cell(f'E{self.data_row + 1}', best_streak, scores) #Best Streak update

def update_cell(cell, value, scores):
    """ 
        Updates cell on scores sheet
    """
    scores.update(cell, value)

def get_data():
    """ 
        Gets the spreadsheet and the cell data from the Google sheet
        and returns a list with the cell values and the scores sheet
    """
    scores = SHEET.worksheet('Scores')
    all_values = scores.get_all_values()
    return [all_values, scores]

def get_random(size):
    '''
        generates a random number between 1 and the
        size of the board
    '''
    return random.randint(0, size)

def generate_coords(size):
    '''
        Generates random x and y coordinates
        and returns them in a list.
    '''
    random_row = get_random(size)
    random_col = get_random(size)
    return [random_row, random_col]

def build_boards(valid_input, player_name):
    '''
        Using the user input creates both boards from the create_game_board class
        and returns a list with the player board and computer
        board
    '''
    my_board = create_game_board( valid_input[0], valid_input[1], player_name )
    my_board.add_ships()
    computer_board = create_game_board( valid_input[0], valid_input[1] )
    computer_board.add_ships()
    return [my_board, computer_board]

def print_board(board, my_board):
    '''
        Formats the given board matrix into a series of strings and 
        prints out each row in order
    '''

    num_label = 1
    rows = ["  ".join(row) for row in board]

    for row in rows:
        if num_label == my_board.size:
            print(num_label, row)
            break
        print(num_label, row, '\n')
        num_label += 1

def print_boards(my_board, computer_board):
    '''
        Prints both boards with row and columns labeled
        and the hit count over each board
    '''
    print(f"-------- ROUND: {my_board.round_count}. {my_board.whos_turn}'s Turn --------")
    print('PLAYER BOARD, Hits Taken: ', my_board.hit_count, 'of', my_board.ships)
    col_num = 1
    col_labels = '   '
    for _ in range(0, my_board.size):
        col_labels += f'{col_num}   '
        col_num += 1
    print(col_labels)
    print_board(my_board.board_matrix, my_board)
    board_label = f'COMPUTER BOARD, Hits Taken: {computer_board.hit_count} of {computer_board.ships}'
    loading_delay(board_label, 1)
    print(col_labels)
    print_board(computer_board.board_matrix_obscured, my_board)

def loading_delay(message, delay):
    """ 
        Prints a message and creates a delay for a given
        value in seconds
    """
    print(message)
    time.sleep(delay)

def validate_ship_to_board_size_ratio(valid_input):
    '''
        Check that the board area is larger that the number 
        of ships.
        Returns boolean
    '''
    area = valid_input[0] * valid_input[0]
    if area > valid_input[1]:
        return True
    print('**NUMBER OF SHIPS IS TOO BIG FOR THIS BOARD AREA\nREDUCE THE NUMBER OF SHIPS OR INCREACE BOARD SIZE')
    return False

def check_board_size(x):
    '''
        Check that the board is not larger than 9
        Returns boolean
    '''
    if x < 10:
        return True
    print('**BOARD SIZE CANNOT BE BIGGER THAN 9')
    return False

def validate_input(parameters, is_board_built = False):
    '''
        Validates input by checking if there is more than one parameter,
        that only numbers are input, the board size, and board size to
        ship ratio is correct.
        Returns valid input in seperate values and in integer form in a
        list or False if input is not valid.
    '''
    if is_command(parameters):
        return False

    parameters = parameters.split()
    try:
        x = int(parameters[0])
    except ValueError:
        print('**FIRST PARAMETER IS NOT A NUMBER')
        return False
    except IndexError:
        print('**NOTHING WAS ENTERED. TRY AGAIN')
        return False
    try:
        y = int(parameters[1])
        if is_board_built:
             return [x, y]
        if validate_ship_to_board_size_ratio([x, y]) and check_board_size(x):
            return [x, y]
    except ValueError:
        print('**SECOND PARAMETER IS NOT A NUMBER')
        return False
    except IndexError:
        print('**ONLY ONE PARAMETER WAS ENTERED. TRY AGAIN')
        return False
    return False

def is_off_board(coords, board):
    '''
        Checks if the coordinates entered were off the board.
        Returns True if it is with an error message.
    '''
    if coords[0] > board.size:
        print('**X COORDINATE IS OFF BOARD! VALUE MUST BE', board.size, 'OR LESS')
        return True
    if coords[1] > board.size:
        print('**Y COORDINATE IS OFF BOARD! VALUE MUST BE', board.size, 'OR LESS')
        return True
    return False

def is_command(parameters):
    """ 
        Checks if a pre defined command has been passed
        to the console and runs it if it has been passed.
        Returns boolean to indicate presence of command.
    """
    if clear_console(parameters):
        return True
    if print_instructions(parameters):
        return True
    if print_score_board(parameters):
        return True
    return False

def print_instructions(parameter = 'help'):
    """ 
        Prints help information if parameter passed is equal to string 'Help' or 'help'.
        Parameter passed is equal to 'help' by default.
        Returns boolean indicating presence of defined string.
    """
    if parameter == 'help' or parameter == 'Help':
        print('GAME INSTRUCTIONS:')
        print('Legend:\nSHIP  - <>\nSUNKEN SHIP - #\nMISS - X\nNOT YET FIRED UPON - .\n')
        print('To Fire enter coordinates seperated by a space.\nThe top left coordinate is 1 1.\n')
        print('For help at any time type "help". To see\nthe score board type "scores". Clear\nthe console type "clear".\n')
        return True
    return False

def sort_scores(score):
    """
        Helper function for sort() method to sort scores
    """
    return score.get('score')

def clear_console(parameters = 'clear'):
    """
        Clears the console if parameter passed is equal to string 'Clear' or 'clear'.
        Parameter passed is equal to 'clear' by default.
        Returns boolean indicating presence of defined string.
    """
    if parameters == 'clear' or parameters == 'Clear':
        os.system('clear')
        return True
    return False

def print_score_board(parameters = 'scores'):
    """
        Prints the tops 5 best winning streaks from the database if parameter
        passed is equal to string 'Scores' or 'scores'. Parameter passed is
        equal to 'scores' by default.
        Returns boolean indicating presence of defined string.
    """
    if parameters == 'scores' or parameters == 'Scores':
        data = get_data()[0]
        scores = [{ 'name': row[0], 'score': row[4] } for row in data]
        scores.sort(key=sort_scores, reverse=True)
        print('**TOP 5 BEST WINNING STREAKS**')
        index = 1
        length = len(scores)
        if length > 5:
            length = 6
        for row in range(1, length):
                print(f'{scores[index]["name"]}: {scores[index]["score"]}')
                index += 1
        print('\n')
        return True
    return False

def setup_game():
    """
        Collects game info; board size, ship number, player name.
        Builds the game boards from the user input.
        Sets the turn and prints the boards.
        Returns 2 board objects in a list. 
    """
    valid_input = False
    print('First enter board size first and then the\nnumber of ships, seperated by a space. eg. 2 3')
    while not valid_input:
        board_info = input('Board size cannot be bigger than 9:\n')
        valid_input = validate_input(board_info)
    player_name = input('Enter your name:\n')
    game_boards = build_boards(valid_input, player_name)
    my_board = game_boards[0]
    computer_board = game_boards[1]
    track_rounds('nobody', my_board, computer_board)
    print_boards(my_board, computer_board)
    return [my_board, computer_board]

def track_rounds(current_player, my_board, computer_board):
    '''
        Toggles between player and computer to keep track of turns
        and updates player object with turn and round data.
        Returns current turn player. 
    '''
    my_board.turn_count += 1
    my_board.round_count = math.ceil(my_board.turn_count / 2)
    if current_player == my_board.name:
        my_board.whos_turn = computer_board.name
        return computer_board.name
    my_board.whos_turn = my_board.name
    return my_board.name 

def end_game(my_board, computer_board):
    """
        Checks to see who won at the end of the game,
        Prints the appropriate message, updates
        the database, and runs a new game.

    """
    if my_board.hit_count < computer_board.hit_count:
        print('********** (: HURRAY!!! YOU WIN :) **********')
        my_board.update_player_scores(1, 0)
    else:
        print('********** ): YOU LOSE :( **********')
        my_board.update_player_scores(0, 1)
    run_game()

def run_game():
    """
        Main game loop that handles the flow of the program.
    """
    print_score_board()
    print_instructions()

    game_boards = setup_game()
    my_board = game_boards[0]
    computer_board = game_boards[1]

    current_turn = my_board.whos_turn

    while my_board.hit_count < my_board.ships and computer_board.hit_count < computer_board.ships:
        unique_coords = False
        while not unique_coords:
            targeting = ''
            if current_turn == my_board.name:
                valid_input = False
                while not valid_input:
                    coords = input('------ ENTER COORDINATES. eg. 2 3 --------\n')
                    valid_input = validate_input(coords, True)
                if is_off_board(valid_input, my_board) == True:
                    break
                targeting = computer_board.recieve_shot(valid_input[0], valid_input[1])
            if current_turn == computer_board.name:
                valid_input = generate_coords(computer_board.size)
                targeting = my_board.recieve_shot(valid_input[0], valid_input[1])
            if targeting == '**ALREADY FIRED ON THESE COORDINATES. TRY AGAIN':
                if current_turn == my_board.name:
                    print(targeting)
                unique_coords = False
            if targeting == 'Hit' or targeting == 'Miss':
                targeting_message = f'{current_turn} Targeting: {targeting}'
                loading_delay(targeting_message, 2)
                current_turn = track_rounds(current_turn, my_board, computer_board)
                unique_coords = True
        print_boards(my_board, computer_board)
    end_game(my_board, computer_board)

run_game()

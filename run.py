import copy
import gspread
from numpy import random
from pprint import pprint
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

    def build_board(self):
        '''
        builds the board matrix according to size
        '''

        for row in range( 0, self.size ):
            row_list = []
            for col in range( 0, self.size ):
                row_list.append(' .')
            self.board_matrix.append(row_list)
            row_list = []
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
        data = get_data()
        all_values = data[0]
        scores = data[1]
        pword = input('New player! Enter a password:\n')
        length = len(all_values)
        self.current_history = all_values[length - 1]
        name_cell = f'A{length + 1}'
        wins_cell = f'B{length + 1}'
        losses_cell = f'C{length + 1}'
        streak_cell = f'D{length + 1}'
        best_streak_cell = f'E{length + 1}'
        pword_cell = f'F{length + 1}'
        scores.update(name_cell, self.name)
        scores.update(wins_cell, 0)
        scores.update(losses_cell, 0)
        scores.update(streak_cell, 0)
        scores.update(best_streak_cell, 0)
        scores.update(pword_cell, pword)

    def login_player(self):
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
                print('Password Incorrect')
                run_game()

    def update_player_scores(self, win, loss):
        self.find_player_row()
        scores = get_data()[1]
        win_update = int(self.current_history[1]) + int(win)
        loss_update = int(self.current_history[2]) + int(loss)
        scores.update(f'B{self.data_row + 1}', win_update)
        scores.update(f'C{self.data_row + 1}', loss_update)
        if loss == 1:
            scores.update(f'D{self.data_row + 1}', 0)
        elif win == 1:
            streak_update = int(self.current_history[3]) + int(1)
            scores.update(f'D{self.data_row + 1}', streak_update)
        all_values = get_data()[0]
        if int(all_values[self.data_row][3]) > int(self.current_history[4]):
            current_streak = int(all_values[self.data_row][3])
            scores.update(f'E{self.data_row + 1}', current_streak)

def get_data():
    scores = SHEET.worksheet('Scores')
    all_values = scores.get_all_values()
    return [all_values, scores]

def get_random(size):
    '''
        generates a random number between 1 and the
        size of the board
    '''
    return random.randint(0, size)

def build_boards(valid_input, player_name):
    '''
        Using the user input creates both boards from the create_game_board class
        and returns an array with the player board and computer
        board
    '''
    my_board = create_game_board( valid_input[0], valid_input[1], player_name )
    my_board.add_ships()
    computer_board = create_game_board( valid_input[0], valid_input[1] )
    computer_board.add_ships()
    return [my_board, computer_board]

def print_board(board):
    '''
        Formats the given board matrix row into a series of strings and 
        prints out each row in order
    '''
    rows = []
    num_label = 1
    for row in board:
        x = "  ".join(row)
        rows.append(x)
    for row in rows:
        print(num_label, row, '\n')
        num_label += 1

def print_boards(my_board, computer_board):
    '''
        Prints both boards with row and columns labeled
        and the hit count over each board
    '''
    print('PLAYER BOARD \nHits Taken: ', my_board.hit_count, 'of', my_board.ships)
    col_num = 1
    col_labels = '   '
    for _ in range(0, my_board.size):
        col_labels += f'{col_num}   '
        col_num += 1
    print(col_labels)
    print_board(my_board.board_matrix)
    print('COMPUTER BOARD: \nHits Taken: ', computer_board.hit_count, 'of', computer_board.ships)
    print(col_labels)
    print_board(computer_board.board_matrix_obscured)

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
        Returns valid input in seperate values and in integer form or
        False if input is not valid
    '''
    
    if print_instructions(parameters):
        return False
    if print_score_board(parameters):
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
    
def whos_turn(current_player):
    '''
        Toggles between player and computer to keep track of turns
    '''
    if current_player == 'PLAYER':
        return 'COMPUTER'
    return 'PLAYER' 

def generate_coords(size):
    '''
        Generates random x and y coordinates
    '''
    random_row = get_random(size)
    random_col = get_random(size)
    return [random_row, random_col]

def print_instructions(parameters = 'help'):
    if parameters == 'help' or parameters == 'Help':
        print('LEGEND: <> - SHIP, # - SUNKEN SHIP, X - MISS, . - NOT YET FIRED UPON')
        return True
    return False

def sort_scores(score):
    return score.get('score')


def print_score_board(parameters = 'scores'):
    if parameters == 'scores' or parameters == 'Scores':
        scores = []
        data = get_data()[0]
        for row in data:
            scores.append( { 'name': row[0], 'score': row[4] } )
        scores.sort(key=sort_scores, reverse=True)
        print('**TOP 5 BEST WINNING STREAKS**')
        index = 1
        for row in range(0, 5):
            if index == 1:
                print(f'{scores[index]["name"]}: {scores[index]["score"]} 🏆')
                index += 1
            print(f'{scores[index]["name"]}: {scores[index]["score"]}')
            index += 1
        print('\n')
        return True
    return False

def end_round(my_board, computer_board):
    if my_board.hit_count < computer_board.hit_count:
        print('********** 😀 HURRAY!!! YOU WIN 😀 **********')
        my_board.update_player_scores(1, 0)
    else:
        print('********** ): YOU LOSE :( **********')
        my_board.update_player_scores(0, 1)
    run_game()

def setup_game():
    valid_input = False
    print('Enter board size first\nand then the number of ships,\nseperated by a space. eg. 2 3')
    while not valid_input:
        board_info = input('Board size cannot be bigger than 9:\n')
        valid_input = validate_input(board_info)
    player_name = input('Enter your name:\n')
    game_boards = build_boards(valid_input, player_name)
    my_board = game_boards[0]
    computer_board = game_boards[1]
    print_boards(my_board, computer_board)
    print_instructions()
    return [my_board, computer_board]

def run_game():
    print_score_board()
    current_turn = 'PLAYER'

    game_boards = setup_game()
    my_board = game_boards[0]
    computer_board = game_boards[1]

    while my_board.hit_count < my_board.ships and computer_board.hit_count < computer_board.ships:
        unique_coords = False
        print('Enter coordinates seperated by\na space to try to make a hit.\nThe top left coordinate is 1 1')
        while not unique_coords:
            targeting = ''
            if current_turn == 'PLAYER':
                valid_input = False
                while not valid_input:
                    coords = input('eg. 2 3: \n')
                    valid_input = validate_input(coords, True)
                if is_off_board(valid_input, my_board) == True:
                    break
                targeting = computer_board.recieve_shot(valid_input[0], valid_input[1])
            if current_turn == 'COMPUTER':
                valid_input = generate_coords(computer_board.size)
                targeting = my_board.recieve_shot(valid_input[0], valid_input[1])
            if targeting == '**ALREADY FIRED ON THESE COORDINATES. TRY AGAIN':
                if current_turn == 'PLAYER':
                    print(targeting)
                unique_coords = False
            if targeting == 'Hit' or targeting == 'Miss':
                current_turn = whos_turn(current_turn)
                print(current_turn, 'TARGETING: ', targeting)
                unique_coords = True
        print_boards(my_board, computer_board)
    end_round(my_board, computer_board)

run_game()

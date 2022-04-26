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
        self.check_score_history()

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

    def check_score_history(self):
        print(self.name)
        scores = SHEET.worksheet('Scores')
        data = scores.get_all_values()
        index = -2
        player_history = []
        for row in data:
            try:
                index = row.index(self.name)
                player_history = row
                break
            except ValueError:
                index = -1
        if index == -1:
            print('NAME NOT FOUND')
        elif index > -1:
            print('PREVIOUS SCORES: ','WINS', player_history[1], 'LOSSES', player_history[2])
        """ scores.update('B2', "test")
        pprint(data) """


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

    parameters = parameters.split()
    try:
        x = int(parameters[0])
    except ValueError:
        print('**FIRST PARAMETER IS NOT A NUMBER')
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
        print('**X COORDINATE IS OFF BOARD! VALUE MUST BE',board.size, 'OR LESS')
        return True
    if coords[1] > board.size:
        print('**Y COORDINATE IS OFF BOARD! VALUE MUST BE',board.size, 'OR LESS')
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

def run_game():
    valid_input = False
    current_turn = 'PLAYER'
    while not valid_input:
        board_info = input('Enter board size first\nand then the number of ships,\nseperated by a space. eg. 2 3 \nBoard size cannot be bigger than 9:\n')
        valid_input = validate_input(board_info)
    player_name = input('Enter your name:\n')
    game_boards = build_boards(valid_input, player_name)
    my_board = game_boards[0]
    computer_board = game_boards[1]
    print_boards(my_board, computer_board)
    
    while my_board.hit_count < my_board.ships and computer_board.hit_count < computer_board.ships:
        valid_input = False
        unique_coords = False
        print('Enter coordinates seperated by\na space to try to make a hit.\nThe top left coordinate is 1 1')
        while not valid_input or not unique_coords:
            targeting = ''
            if current_turn == 'PLAYER':
                coords = input('eg. 2 3: \n')
                valid_input = validate_input(coords, True)
                if valid_input == False:
                    break
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
    if my_board.hit_count < computer_board.hit_count:
        print('********** XD HURRAY!!! YOU WIN XD **********')
    else:
        print('********** ): YOU LOSE :( **********')
    run_game()

run_game()

from numpy import random, isnan
import copy

class create_game_board:
    def __init__(self, size, ships):
        self.size = size
        self.ships = ships
        self.board_matrix = []
        self.board_matrix_obscured = []
        self.hit_count = 0 

    def build_board(self):
        """
        builds the board matrix according to size
        """

        for row in range( 0, self.size ):
            row_list = []
            for col in range( 0, self.size ):
                row_list.append(' .')
            self.board_matrix.append(row_list)
            row_list = []
        self.board_matrix_obscured = copy.deepcopy(self.board_matrix)
    def add_ships(self):
        """
        adds ships to unique random coordinates according to ship number
        """

        self.build_board()
        for _ in range(0, self.ships):
            done = False
            while not done:
                random_row = get_random(self.size)
                random_col = get_random(self.size)
                if self.board_matrix[random_row][random_col] != '<>':
                    self.board_matrix[random_row][random_col] = '<>'
                    done = True

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
            return 'Already fired on these coordinates. Try again'

def get_random(size):
    '''
        generates a random number between 1 and the
        size of the board
    '''
    return random.randint(0, size)

def build_boards(valid_input):
    my_board = create_game_board( valid_input[0], valid_input[1] )
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
    print('Player Board: \nHits Taken: ', my_board.hit_count, 'of', my_board.ships)
    col_num = 1
    col_labels = '   '
    for _ in range(0, my_board.size):
        col_labels += f'{col_num}   '
        col_num += 1
    print(col_labels)
    print_board(my_board.board_matrix)
    print('Computer Board: \nHits Taken: ', computer_board.hit_count, 'of', computer_board.ships)
    print(col_labels)
    print_board(computer_board.board_matrix_obscured)

def validate_input(parameters):
    '''
        Checks if there is more than one parameter and that
        only numbers are input.
    '''
    parameters = parameters.split()
    try:
        x = int(parameters[0])
    except ValueError:
        print('First parameter is not a number')
        return False
    try:
        y = int(parameters[1])
        return [x, y]
    except ValueError:
        print('Second parameter is not a number')
        return False
    except IndexError:
        print('Only one parameter was entered. Try again')
        return False

def is_off_board(coords, board):
    '''
        Checks if the coordinates entered were off the board.
        Returns True if it is with an error message.
    '''
    if coords[0] > board.size:
        print('X coordinate given is off board! Try again')
        return True
    if coords[1] > board.size:
        print('Y coordinate given is off board! Try again')
        return True
    return False
    
def whos_turn(current_player):
    if current_player == 'Player':
        return 'Computer'
    return 'Player' 

def generate_coords(size):
    random_row = get_random(size)
    random_col = get_random(size)
    return [random_row, random_col]

def run_game():
    valid_input = False
    current_turn = 'Player'
    while not valid_input:
        board_info = input('Enter board size first and the number of ships. eg. 2 3: \n')
        valid_input = validate_input(board_info)

    game_boards = build_boards(valid_input)
    my_board = game_boards[0]
    computer_board = game_boards[1]
    print_boards(my_board, computer_board)
    
    while my_board.hit_count < my_board.ships and computer_board.hit_count < computer_board.ships:
        valid_input = False
        unique_coords = False
        print('Enter coordinates seperated by a space to try to make a hit. The top left coordinate is 1 1')
        while not valid_input or not unique_coords:
            targeting = ''
            if current_turn == 'Player':
                coords = input('eg. 2 3: \n')
                valid_input = validate_input(coords)
                if valid_input == False:
                    break
                if is_off_board(valid_input, my_board) == True:
                    break
                targeting = computer_board.recieve_shot(valid_input[0], valid_input[1])
            if current_turn == 'Computer':
                valid_input = generate_coords(computer_board.size)
                targeting = my_board.recieve_shot(valid_input[0], valid_input[1])
            if targeting == 'Already fired on these coordinates. Try again':
                if current_turn == 'Player':
                    print(targeting)
                unique_coords = False
            if targeting == 'Hit' or targeting == 'Miss':
                current_turn = whos_turn(current_turn)
                print(current_turn, 'Targeting: ', targeting)
                unique_coords = True
        print_boards(my_board, computer_board)
    if my_board.hit_count < computer_board.hit_count:
        print('********** XD HURRAY!!! YOU WIN XD **********')
    else:
        print('********** ): YOU LOSE :( **********')

run_game()

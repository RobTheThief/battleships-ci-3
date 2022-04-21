
from numpy import random

class create_game_board:
    def __init__(self, size, ships):
        self.size = size
        self.ships = ships
        self.board_matrix = []
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
        if self.board_matrix[row - 1][col - 1] == '<>':
            self.board_matrix[row - 1][col - 1] = ' #'
            self.hit_count += 1
        else:
            self.board_matrix[row - 1][col - 1] = ' X'

def get_random(size):
    '''
        generates a random number between 1 and the
        size of the board
    '''
    return random.randint(1, size)

def print_board(board):
    '''
        Formats the given board matrix row into a series of strings and 
        prints out each row in order
    '''
    rows = []
    for row in board:
        x = "  ".join(row)
        rows.append(x)
    for row in rows:
        print(row, '\n')

def run_game():
    my_board = create_game_board( 6, 7 )
    my_board.add_ships()
    print_board(my_board.board_matrix)
    my_board.recieve_shot(3,3)
    print_board(my_board.board_matrix)
    print(my_board.hit_count)
    print('hi')


run_game()

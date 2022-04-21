
from numpy import random

class create_game_board:
    def __init__(self, size, ships):
        self.size = size
        self.ships = ships

    def build_board(self):
        """
        builds the board to be printed
        """

        board_matrix = []
        for row in range( 0, self.size ):
            row_list = []
            for col in range( 0, self.size ):
                row_list.append('.')
            board_matrix.append(row_list)
            row_list = []
        return board_matrix


def get_random(size):
    '''
        generates a random number between 1 and the
        size of the board
    '''
    return random.randint(1, size)


def print_board(board):
    rows = []
    for row in board:
        x = "   ".join(row)
        rows.append(x)
    for row in rows:
        print(row, '\n')

def run_game():
    my_board = create_game_board( 6, 4 )
    print_board(my_board.build_board())
    print(get_random(my_board.size))


run_game()

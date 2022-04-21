
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


def run_game():
    my_board = create_game_board( 5, 4 )
    print(my_board.build_board())


run_game()

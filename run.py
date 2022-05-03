import copy

from library import helpers, api_calls


class GameBoard:
    def __init__(self, size, ships, name='Computer'):
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
        for row in range(0, self.size):
            row_list = [' .' for cell in range(0, self.size)]
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
                random_row = helpers.get_random(self.size)
                random_col = helpers.get_random(self.size)
                if self.board_matrix[random_row][random_col] != '<>':
                    self.board_matrix[random_row][random_col] = '<>'
                    done = True
        if self.name != 'Computer':
            self.login_player()

    def recieve_shot(self, row, col):
        '''
            checks if given coordinates are a hit or miss and updates the board
        '''
        target = self.board_matrix[row - 1][col - 1]
        if target == '<>':
            self.board_matrix[row - 1][col - 1] = ' #'
            self.board_matrix_obscured[row - 1][col - 1] = ' #'
            self.hit_count += 1
            return 'Hit'
        elif target == ' .':
            self.board_matrix[row - 1][col - 1] = ' X'
            self.board_matrix_obscured[row - 1][col - 1] = ' X'
            return 'Miss'
        elif target == ' X' or target == ' #':
            return '**ALREADY FIRED ON THESE COORDINATES. TRY AGAIN'

    def find_player_row(self):
        """
            Finds which row the players data is on
            and saves the data and the row number to
            the board object.
        """
        data = api_calls.get_data()
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
        data = api_calls.get_data()
        all_values = data[0]
        scores = data[1]
        pword = input('New player! Enter a password:\n')
        length = len(all_values)

        api_calls.update_cell(f'A{length + 1}', self.name, scores)  # Name
        api_calls.update_cell(f'B{length + 1}', 0, scores)  # Wins
        api_calls.update_cell(f'C{length + 1}', 0, scores)  # Losses
        api_calls.update_cell(f'D{length + 1}', 0, scores)  # Current Streak
        api_calls.update_cell(f'E{length + 1}', 0, scores)  # Best Streak
        api_calls.update_cell(f'F{length + 1}', pword, scores)  # Password

        data = api_calls.get_data()
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
                    scores_line_1 = (
                        f'\nWins: {self.current_history[1]} '
                        f'Losses: {self.current_history[2]}'
                    )
                    scores_line_2 = (
                        f'Current win streak: '
                        f'{self.current_history[3]} '
                        f'Best win streak: '
                        f'{self.current_history[4]}'
                    )
                    print(scores_line_1)
                    print(scores_line_2)
                    password_wrong = False
                    break
                helpers.loading_delay('Password Incorrect. Resetting game..', 2)
                run_game()

    def update_player_scores(self, win, loss):
        """
            Updates the database for player for wins, losses, current streak,
            best streak.
        """
        self.find_player_row()
        scores = api_calls.get_data()[1]

        win_update = int(self.current_history[1]) + int(win)
        api_calls.update_cell(f'B{self.data_row + 1}', win_update, scores)  # Wins

        loss_update = int(self.current_history[2]) + int(loss)
        api_calls.update_cell(f'C{self.data_row + 1}', loss_update, scores)  # Lossses

        if loss == 1:
            api_calls.update_cell(
                f'D{self.data_row + 1}', 0, scores
            )  # Current Streak reset to 0
        elif win == 1:
            streak_update = int(self.current_history[3]) + int(1)
            api_calls.update_cell(
                f'D{self.data_row + 1}', streak_update, scores
            )  # C urrent Streak increase
        all_values = api_calls.get_data()[0]
        if int(all_values[self.data_row][3]) > int(self.current_history[4]):
            best_streak = int(all_values[self.data_row][3])
            api_calls.update_cell(
                f'E{self.data_row + 1}', best_streak, scores
            )  # Best Streak update


def run_game():
    """
        Main game loop that handles the flow of the program.
    """
    helpers.print_game_start_help()

    game_boards = helpers.setup_game(GameBoard) ## CHANGE NAME HERE
    my_board = game_boards[0]
    computer_board = game_boards[1]

    current_turn = my_board.whos_turn

    while ( ### ADD TO BUSINESS LOGIC
            my_board.hit_count < my_board.ships and
            computer_board.hit_count < computer_board.ships
    ):
        unique_coords = False
        while not unique_coords:
            targeting = ''
            if current_turn == my_board.name:
                valid_input = False
                while not valid_input:
                    coords = input(
                        '------ ENTER COORDINATES. eg. 2 3 --------\n')
                    valid_input = helpers.validate_input(coords, True)
                if helpers.is_off_board(valid_input, my_board):
                    break
                targeting = computer_board.recieve_shot(
                    valid_input[0], valid_input[1])
            if current_turn == computer_board.name:
                valid_input = helpers.generate_coords(computer_board.size)
                targeting = my_board.recieve_shot(
                    valid_input[0], valid_input[1])
            if targeting == '**ALREADY FIRED ON THESE COORDINATES. TRY AGAIN':
                if current_turn == my_board.name:
                    print(targeting)
                unique_coords = False
            if targeting == 'Hit' or targeting == 'Miss':
                targeting_message = f'{current_turn} Targeting: {targeting}'
                helpers.loading_delay(targeting_message, 2)
                current_turn = helpers.track_rounds(
                    current_turn, my_board, computer_board)
                unique_coords = True
        helpers.print_boards(my_board, computer_board)
    helpers.end_game(my_board, computer_board)
    run_game()


helpers.get_function(run_game, 'run_game')
run_game()

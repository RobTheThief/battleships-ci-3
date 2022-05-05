"""
    This module contains the helper functions which make up
    bulk of the package.  It also included the run_game
    function which controls the main game flow.
"""

import math
import time
import os
import pyfiglet
from numpy import random

from battleships import api_calls, boards


def run_game():
    """
        Main game loop that handles the flow of the program.
    """
    clear_console('program command 42')
    print_banner("<*>Battleships<*>")
    print_game_start_help()

    game_boards = setup_boards(boards.GameBoard)
    my_board = game_boards[0]
    computer_board = game_boards[1]

    while not game_over(my_board, computer_board):
        play_turn(my_board, computer_board)
        print_boards(my_board, computer_board)
    end_game(my_board, computer_board)
    run_game()


def play_turn(my_board, computer_board):
    """
        Handles the flow of each turn of the game.
    """
    targeting = ''
    valid_input = True
    current_turn = my_board.whos_turn
    if current_turn == my_board.name:
        valid_input = get_valid_input(my_board)
    if not valid_input:
        return
    if current_turn == my_board.name:
        targeting = computer_board.take_fire(
            valid_input[0], valid_input[1])
    if current_turn == computer_board.name:
        valid_input = generate_coords(computer_board.size)
        targeting = my_board.take_fire(
            valid_input[0], valid_input[1])
    if targeting == '**ALREADY FIRED ON THESE COORDINATES. TRY AGAIN':
        repeat_message(targeting, current_turn)
        return
    if targeting == 'Hit' or targeting == 'Miss':
        targeting_message = f'{current_turn} Targeting: {targeting}'
        pause_message(targeting_message, 2)
        current_turn = track_rounds(
            current_turn, my_board, computer_board)
        return


def repeat_message(targeting, current_turn):
    """
        Prints a message with a delay reporting that
        the coordinates were already fired upon if
        the turn is not the Computers.
    """
    if current_turn != 'Computer':
        pause_message(targeting, 2)


def print_banner(text):
    """
        Prints banner with stylised text.
    """
    ascii_banner = pyfiglet.figlet_format(text)
    print(ascii_banner)


def get_valid_input(my_board):
    """
        Prompts use for input and checks if
        it is in the correct format and data
        type and also if the coordinates are
        useable.
        Returns False if it does not meet the
        requirements.
    """
    bad_coords = False
    coords = input(
                '------ ENTER COORDINATES. eg. 2 3 --------\n')
    valid_input = validate_input(coords, True, my_board)
    if valid_input:
        bad_coords = is_off_board(valid_input, my_board)
    if not bad_coords:
        return valid_input
    return False


def game_over(my_board, computer_board):
    """
        Checkes if the game has been won yet and
        returns boolean.
    """
    if (my_board.hit_count < my_board.ships and
            computer_board.hit_count < computer_board.ships):
        return False
    return True


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


def build_boards(valid_input, player_name, create_game_board):
    '''
        Using the user input creates both boards from the
        create_game_board class and returns a list with the
        player board and computer board
    '''
    my_board = create_game_board(valid_input[0], valid_input[1], player_name)
    my_board.add_ships()
    computer_board = create_game_board(valid_input[0], valid_input[1])
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


def make_col_labels(my_board):
    """
        Makes a string used to label the columns
        on the board with numbers.
    """
    col_num = 1
    col_labels = '   '
    for _ in range(0, my_board.size):
        col_labels += f'{col_num}   '
        col_num += 1
    return col_labels


def print_boards(my_board, computer_board):
    '''
        Prints both boards with row and columns labeled
        and the hit count over each board
    '''
    clear_console('program command 42')
    print(
        f"-------- ROUND: {my_board.round_count}.",
        f"{my_board.whos_turn}'s Turn --------"
    )
    print(
        'PLAYER BOARD, Hits Taken: ',
        my_board.hit_count,
        'of', my_board.ships
    )
    col_labels = make_col_labels(my_board)
    print(col_labels)
    print_board(my_board.board_matrix, my_board)

    board_label = (
        f'COMPUTER BOARD, Hits Taken: '
        f'{computer_board.hit_count} of {computer_board.ships}'
    )
    print(board_label)
    print(col_labels)
    print_board(computer_board.board_matrix_obscured, my_board)


def pause_message(message, delay):
    """
        Prints a message and creates a delay for a given
        value in seconds
    """
    print(message)
    time.sleep(delay)


def validate_ship_quantity(valid_input):
    '''
        Check that the board area is larger that the number
        of ships.
        Returns boolean
    '''
    area = valid_input[0] * valid_input[0]
    if area > valid_input[1]:
        return True
    print(
        '**NUMBER OF SHIPS IS TOO BIG FOR THIS BOARD',
        'AREA\nREDUCE THE NUMBER OF SHIPS OR INCREACE BOARD SIZE'
    )
    return False


def check_board_size(size):
    '''
        Check that the board is not larger than 9
        Returns boolean
    '''
    if size < 10:
        return True
    print('**BOARD SIZE CANNOT BE BIGGER THAN 9')
    return False


def validate_input(parameters, is_board_built=False, my_board={}):
    '''
        Validates input by checking if there is more than one parameter,
        that only numbers are input, the board size, and board size to
        ship ratio is correct.
        Returns valid input in seperate values and in integer form in a
        list or False if input is not valid.
    '''
    if is_command(parameters, my_board):
        return False
    parameters = parameters.split()
    try:
        num_1 = int(parameters[0])
    except ValueError:
        pause_message('**FIRST PARAMETER IS NOT A NUMBER', 2)
        return False
    except IndexError:
        pause_message('**NOTHING WAS ENTERED. TRY AGAIN', 2)
        return False
    try:
        num_2 = int(parameters[1])
        if num_1 <= 0 or num_2 <= 0:
            pause_message('**VALUES CANNOT BE ZERO OR LESS', 2)
            return
        if is_board_built:
            return [num_1, num_2]
        if validate_ship_quantity([num_1, num_2]) and check_board_size(num_1):
            return [num_1, num_2]
    except ValueError:
        pause_message('**SECOND PARAMETER IS NOT A NUMBER', 2)
        return False
    except IndexError:
        pause_message('**ONLY ONE PARAMETER WAS ENTERED. TRY AGAIN', 2)
        return False
    return False


def is_off_board(coords, board):
    '''
        Checks if the coordinates entered were off the board.
        Returns True if it is with an error message.
    '''
    if coords[0] > board.size:
        message = (
            f'**X COORDINATE IS OFF BOARD! VALUE MUST BE '
            f'{board.size} OR LESS'
        )
        pause_message(message, 2)
        return True
    if coords[1] > board.size:
        message = (
            f'**Y COORDINATE IS OFF BOARD! VALUE MUST BE '
            f'{board.size} OR LESS'
        )
        pause_message(message, 2)
        return True
    return False


def is_command(parameters, my_board):
    """
        Checks if a pre defined command has been passed
        to the console and runs it if it has been passed.
        Returns boolean to indicate presence of command.
    """
    if clear_console(parameters):
        return True
    if print_help(parameters):
        return True
    if print_score_board(parameters):
        return True
    if reset_game(parameters):
        return True
    if about(parameters):
        return True
    if my_scores(parameters, my_board):
        return True
    return False


def confirm_input(task):
    """
        Checks with the user that they want to go ahead
        with the defined task.
        Returns boolean.
    """
    answer = input(f'Do you want {task} y / n\n')
    if answer == 'y' or answer == 'Y':
        return True
    return False


def my_scores(parameter='myscores', my_board={}):
    """
        Prints player score info if parameter
        passed is equal to string 'myscores' or
        'Myscores'. Parameter passed is equal to
        'myscores' by default. Returns False if
        there is no presence of defined string.
    """
    if my_board == {}:
        return False
    if parameter == 'myscores' or parameter == 'Myscores':
        print(
                f'Wins: {my_board.current_history[0]}',
                f'\nLosses: {my_board.current_history[1]}',
                f'\nCurrent Streak: {my_board.current_history[2]}',
                f'\nBest Streak: {my_board.current_history[3]}',
        )
        input('Press enter to continue')
        return True
    return False


def about(parameter='about'):
    """
        Prints info about the game if parameter
        passed is equal to string 'about' or
        'About'. Parameter passed is equal to
        'about' by default. Returns False if
        there is no presence of defined string.
    """
    if parameter == 'about' or parameter == 'About':
        print(
            '\n------------ How to play -----------------',
            '\nBattleships is played by guessing the',
            '\ncoordinates of your opponents ships.',
            '\nYou choose your coordinates using numbers',
            '\n1 - 9.  The first number represents a row,',
            '\nor "X" and the second is a column, or "Y.',
            '\nThe first player to destroy all of their',
            '\noppenents ships wins'
            '\n------------------------------------------\n',
        )
        input('Press enter to continue')
        return True
    return False


def reset_game(parameter='reset'):
    """
        Resets the game if parameter passed is equal
        to string 'reset' or 'Reset'. Parameter
        passed is equal to 'reset' by default.
        Returns False if there is no presence of
        defined string.
    """
    confirmed = False
    if parameter == 'reset' or parameter == 'Reset':
        confirmed = confirm_input('to reset the game?')
    if confirmed:
        run_game()
    return False


def print_help(parameter='help'):
    """
        Prints help information if parameter passed is
        equal to string 'Help' or 'help'. Parameter
        passed is equal to 'help' by default.
        Returns boolean indicating presence of defined
        string.
    """
    if parameter == 'help' or parameter == 'Help':
        print('------------ GAME HELP -------------')
        print(
            'Legend:\nSHIP  - <>\nSUNKEN SHIP',
            '- #\nMISS - X\nNOT YET FIRED UPON - .\n'
        )
        print(
            'To Fire enter coordinates seperated by',
            '\na space. The top left coordinate is 1 1.\n')
        print(
            'For help at any time type "help". To',
            '\nsee the score board type "scores".',
            '\nClear the console type "clear". To',
            '\nreset the game type "reset" To',
            '\nlearn more about the game mechanics',
            '\ntype "about."',
        )
        print('------------------------------------\n')
        input('Press enter to continue')
        return True
    return False


def print_game_start_help():
    """
        Prints less verbose help information at the
        beginning of the game.
    """

    print(
        '---------- GAME COMMANDS -----------',
        '\nFor help at any time type "help". To',
        '\nsee the score board type "scores".',
        '\nClear the console type "clear". To',
        '\nreset the game type "reset" To',
        '\nlearn more about the game mechanics',
        '\ntype "about."',
    )
    print('------------------------------------\n')


def clear_console(parameters='clear'):
    """
        Clears the console if parameter passed is equal
        to string 'Clear' or 'clear'. Parameter passed
        is equal to 'clear' by default.
        Returns boolean indicating presence of defined
        string.
    """
    confirmed = False
    if parameters == 'program command 42':
        os.system('clear')
        return True
    if parameters == 'clear' or parameters == 'Clear':
        confirmed = confirm_input('to clear the terminal?')
    if confirmed:
        os.system('clear')
        return True
    return False


def sort_scores(score):
    """
        Helper function for sort() method to sort scores
    """
    return score.get('score')


def print_score_board(parameters='scores'):
    """
        Prints the tops 5 best winning streaks from the database if parameter
        passed is equal to string 'Scores' or 'scores'. Parameter passed is
        equal to 'scores' by default.
        Returns boolean indicating presence of defined string.
    """
    if parameters == 'scores' or parameters == 'Scores':
        data = api_calls.get_sheet_data()[0]
        scores = [{'name': row[0], 'score': row[4]} for row in data]
        scores.sort(key=sort_scores, reverse=True)
        print('-----TOP 5 BEST WINNING STREAKS-----')
        index = 1
        length = len(scores)
        if length > 5:
            length = 6
        for row in range(1, length):
            print(f'{scores[index]["name"]}: {scores[index]["score"]}')
            index += 1
        print('------------------------------------\n')
        input('Press enter to continue')
        return True
    return False


def setup_boards(create_game_board):
    """
        Collects game info; board size, ship number, player name.
        Builds the game boards from the user input.
        Sets the turn and prints the boards.
        Returns 2 board objects in a list.
    """
    valid_input = False
    print(
        '\nIf you enter 4 for size it will be a 4 X 4 board.',
        '\nThe next digit is the number of ships on the board.',
        '\nFirst enter board size and then the number of ships,',
        '\nseperated by a space. Example: 4 5',
    )
    while not valid_input:
        board_info = input('Board size cannot be bigger than 9:\n')
        valid_input = validate_input(board_info)
    player_name = input('Enter your name:\n')
    while player_name == '':
        player_name = input('Name must not be empty:\n')
    game_boards = build_boards(valid_input, player_name, create_game_board)
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
        prints the appropriate message, and updates
        the database.
    """
    if my_board.hit_count < computer_board.hit_count:
        print_banner('You Win! : )')
        my_board.update_player_scores(1, 0)
    else:
        print_banner('You Lose! : (')
        my_board.update_player_scores(0, 1)

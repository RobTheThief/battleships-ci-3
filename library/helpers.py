import math
import time
import os
from numpy import random

from library import api_calls

FUNCS = {}


def get_function(func, func_name):
    """
        Takes in a function and a string and saves the
        string as a key and the function as a value in
        the global dictionary FUNC.
    """
    FUNCS[func_name] = func


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
    clear_console()
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
    print(
        '**NUMBER OF SHIPS IS TOO BIG FOR THIS BOARD',
        'AREA\nREDUCE THE NUMBER OF SHIPS OR INCREACE BOARD SIZE'
    )
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


def validate_input(parameters, is_board_built=False):
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
        print(
                '**X COORDINATE IS OFF BOARD! VALUE MUST BE',
                board.size, 'OR LESS'
        )
        return True
    if coords[1] > board.size:
        print(
                '**Y COORDINATE IS OFF BOARD! VALUE MUST BE',
                board.size, 'OR LESS'
        )
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
    if print_help(parameters):
        return True
    if print_score_board(parameters):
        return True
    if reset_game(parameters):
        return True
    if about(parameters):
        return True
    return False


def about(parameter='about'):
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
    if parameter == 'reset' or parameter == 'Reset':
        answer = input('Are you sure you want to reset this game? y / n\n')
        if answer == 'y':
            FUNCS['run_game']()
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
    if parameters == 'clear' or parameters == 'Clear':
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
        data = api_calls.get_data()[0]
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
        return True
    return False


def setup_game(create_game_board):
    """
        Collects game info; board size, ship number, player name.
        Builds the game boards from the user input.
        Sets the turn and prints the boards.
        Returns 2 board objects in a list.
    """
    valid_input = False
    print(
            'First enter board size first and then',
            'the\nnumber of ships, seperated by a space. eg. 2 3'
    )
    while not valid_input:
        board_info = input('Board size cannot be bigger than 9:\n')
        valid_input = validate_input(board_info)
    player_name = input('Enter your name:\n')
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
        print('********** (: HURRAY!!! YOU WIN :) **********')
        my_board.update_player_scores(1, 0)
    else:
        print('********** ): YOU LOSE :( **********')
        my_board.update_player_scores(0, 1)

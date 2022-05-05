# Battleships Command Line Game

A remake of the popular pen and paper game Battleships in the command line.
Boards are printed out using keyboard characters in a matrix. It uses the
Google Sheets API to access a Google sheet and keep scores for players. 

![Responsive Mockup](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/responsive_mockup_battleships.png)

## User Experience (UX)

- ### User stories

  - #### First Time Visitor Goals

    1. As a First Time Visitor, I want to understand clearly the game mechanics.
    2. As a First Time Visitor, I want to understand the game controls.
    3. As a First Time Visitor, I want to be able keep track of score.

  - #### Returning Visitor Goals

    1. As a Returning Visitor, see my previous scores and play again.

- ### Design
  The game is entirely command line based and so the styling is restricted to the  
  terminal it runs on.
  - #### Wireframe
    - This wireframe was used initially to get an idea how the game would look in the terminal:
      ![Wireframe Screenshot](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/battleships-ci-3_wireframe.png)
  - #### Logic Flow Chart
    - This flow chart was used initially to work out the logic of the game:
      ![Flow chart Screenshot](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/logic_flowchart.png)

## FEATURES

### EXISTING FEATURES

- **Score board**

  - Ability to add player name to keep track of score by means of a cloud based database.  
  The score board through game commands `scores` and `myscores`.

  ![Score board](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/score_board.png)
  ![Player scores](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/myscores.png)

  - The player enters their name and password.
  - Password must match if it was a previously used name.
  - A new entry is made in the Google sheets database if the name has not been used before.

  ![Login](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/user_password.png)

  ![Google Sheets](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/google_sheet_sample.png)
  Sample of the google sheet used for this project

- **Choose board size and ship number** 

  - At the beginning of the game the user is prompted to enter two numbers; The size of the board and the number of ships. 

  ![Choose board size and ship number](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/set_size_and_ships.png)

- **Coordinate based input**

  - Using the row and column, or X, Y the player can enter the coordinates to fire upon.

  ![Coordinate input](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/coordinates.png)

- **Play against the computer**

  - The player plays against the computer. Unique random coordinates are generated by the program and used to
  take a shot at the players board.
  - The computers board is obscured so that you cannot see the ships.

  ![Player vs Computer](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/player_v_computer.png)

- **Random ship placement**

  - After the board is created random coordinates are created and used to place the correct number of ships.

  ![Random ship placement](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/random_ship_placement.png)

- **In Game Commands**

  - After the game starts instead of entering coordinates the player can enger 4 different commands
    1. "help" is used to print out the game instructions.
    1. "scores" is used to print out the score board.
    1. "myscores" is used to print out the players score history.
    1. "reset" is used to reset the game. The player is asked to confirm command first.
    1. "about" is used to learn more about the game mechanics if you are unfamiliar with Battleships.  
    as well as developer information.

  ![Game Commands](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/game_commands.png)

### FUTURE FEATURES

- **PvP**

  - A possible future feature might be to allow players to log into a  
  lobby and match up to play against each other.


## Technologies Used

### Languages Used

- [Python](https://en.wikipedia.org/wiki/Python_(programming_language))

### Libraries & Programs Used

#### Python Librarys

1. [gspread:](https://docs.gspread.org/)
    - This library is used to access and update the the data in the spreadsheet. 
1. [google-auth:](https://google-auth.readthedocs.io/en/master/)
    - google-auth is the Google authentication library for Python. This library  
    provides the ability to authenticate to Google APIs.
1. [copy:](https://docs.python.org/3/library/copy.html)
    - This library is used to make a deep copy of the the board matrix and not  
    just a reference to the location in memeory.
1. [math:](https://docs.python.org/3/library/math.html)
    - The math library is used to implement `math.ceil()` to round up a number  
    in determining the game round number. 
1. [time:](https://docs.python.org/3/library/time.html)
    - time was used to create a delay between prints so that the user could see  
    the information as it was printed with `time.sleep(delay)`
1. [os:](https://docs.python.org/3/library/os.html)
    - Here os was used so that it was possible to run the `clear` terminal  
    command from the program using `os.system()`
1. [numpy:](https://numpy.org/)
    - numpy was used to generate the random numbers needed for the random  
    coordinates and the random placement of the ships.
1. [pyfiglet:](https://github.com/pwaller/pyfiglet)
    - pyfiglet was used to generate the game logo graphic. 
1. [getpass:](https://docs.python.org/3/library/getpass.html)
    - getpass was used to conceal the password input by the user.

#### Programs

1. [Git](https://git-scm.com/)
   - Git was used for version control by utilizing the Gitpod terminal to commit  
   to Git and Push to GitHub.
1. [GitHub:](https://github.com/)
   - GitHub is used to store the projects code after being pushed from Git.
1. [Heroku:](https://www.heroku.com/)
   - Was used to host and deploy the game.
1. [Lucid:](https://www.lucidchart.com/)
   - Was used to make the logic flow chart in this readme.
1. [Balsamiq:](https://balsamiq.com/)
   - Was used to create the wireframe for the game.
1. [Google Sheets](https://en.wikipedia.org/wiki/Google_Sheets)
   - Google sheets was used as a simple database to store player  
   score history. 


## TESTING

### Testing User Stories from User Experience (UX) Section

- #### First Time Visitor Goals

  1. As a First Time Visitor, I want to understand clearly the game mechanics.
     1. When the game loads there are instructions on how to set up the game. 
     2. When the game loads there are instructions on how to use game commands and in  
     particular there are 'help' and 'about' commands that give an even more detailed  
     discription of how to play the game. 
     3. A legend is provided through using the help command.
  2. As a First Time Visitor, I want to understand the game controls.
     1. The 'about' command will describe how the coordinates work.
     2. The introduction information and the 'help' command describe how to enter  
     coordinates.
     3. Upon being prompted for input an example is given.
  3. As a First Time Visitor, I want to be able keep track of score.
     1. Every time a shot is fired 'Hit' or 'Miss' is printed. 
     2. Each board has the number of hits taken displayed in each turn.
     3. At the end of the game the results are recorded to the database.
     4. The user can type 'scores' at any time to see the top 5 best winning streaks  
     from past users.

- #### Returning Visitor Goals

  1. As a Returning Visitor, see my previous scores and play again.
     1. When the user logs in again their entire score history is printed.
     2. The user can type 'scores' at any time to see the top 5 best winning streaks  
     from past users.
     3. The user can type 'myscores' at any time to see their score history.
     4. At the end of the game the results are recorded to the database.

### Known Bugs

#### Solved Bugs

- Having split the code up into modules the run_game function needed to me accessible  
in helpers but importing run.py into helpers caused a circular import error.
  - I decided to create a package with all the modules in it and only use  
    run.py to import and run run_game(). This gave the other functions access  
    to the run_game function.

- Entering zero or minus values gave unusual bugs like doind so for borad  
size and ship number and then logging in the game would immediatly declare that you  
lost the game and start a new one.
- Doing so during the game when entering coordinates would result in random  
coordinates being fired upon.
  - For both of these bugs the solution was to add a check into the validate_input  
  function for zero or minus integers.

#### Remaining Bugs

- No remaining bugs found.

### Further Testing

- Tested locally and on the Code Institute Heroku terminal.
- Test giving the program invalid input; strings, off board values, too many  
ships for board size, board size too big, negative and zero values, no input.
- Friends and family members were asked to play the game to point  
out any bugs and/or user experience issues.

### Validator Testing

  - PEP8

    Validations errors that were found consisted mainly of 'Trailing whitespace' errors  
    and 'line too long' errors and one "comparison to True should be 'if cond is True:'
    or 'if cond:'".  

    White spaces were simply deleted. Line too long errors were solved mainly by  
    breaking up f stings and using parenthesis to enclose them, as well as editing  
    docstrings. The comparison error was solved by simply deleting '== True' as this  
    was redundant.

    All three files passed the PEP8 validator tests:
    
    **run.py**
    ![Run](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/run_pep8.png)

    **api_calls.py**
    ![API](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/api_pep8.png)

    **helpers.py**
    ![Helpers](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/helpers_pep8.png)

    **boards.py**
    ![Boards Class](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/boards_pep8.png)

    **__init__.py**
    ![__init__](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/init_pep8.png)

  - Vscode Pylint

    An example of one resolved pylint error was:  
    "Sequence index is not an int, slice, or instance with __index__".

    This was resolved by converting the data type passed as index to type int.

    All pylint errors were also resolved:

    **pylint**  

    ![pylint](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/pylint.png)


## Deployment

- Local deployment was achieved with with Python from the console. The game was  
developed on a Ubuntu OS and so was already installed. Steps are as follows:
  - Run `python3 run.py` in the terminal with root directory of the project.

- Heroku Deployment:
    - Create a new Heroku app.
    - Set the build packs to `Python` and `NodeJS` in that order.
    - Set Config Vars key value pairs for:
      1. `PORT`: `8000`
      1. `CREDS`: `{CREDS Object}` where {CREDS Object} is from the credentials file
      dowoloaded from Google Cloud Platform.
    - Enter `heroku login -i` command in the terminal with root directory of the project.
    - Enter Heroku username and password.
    - Enter `git push --set-upstream https://git.heroku.com/battleships-ci-3.git main` to deploy.
    - Enter `git push --set-upstream https://github.com/RobTheThief/battleships-ci-3.git main` to reset upstream to github.

The live link can be found here - https://battleships-ci-3.herokuapp.com/

## Credits
  
  The Code Institute Heroku console was used to deploy the game.

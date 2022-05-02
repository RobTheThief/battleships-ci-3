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
  The score board is viewed at the beginning of each game or through game commands.

  ![Score board](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/score_board.png)

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
    1. "help" is used to print out the game instructions that were printed at the beginning of the game.
    1. "scores" is used to print out the score board that was used at the begining of the game.
    1. "reset" is used to reset the game. The player is asked to confirm command first.
    1. "clear" is used to clear the visible console.
    1. "about" is used to learn more about the game mechanics if you are unfamiliar with Battleships.

  ![Random ship placement](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/game_commands.png)

## Technologies Used

### Languages Used

- [PYTHON](https://en.wikipedia.org/wiki/Python_(programming_language))
- [GOOGLE SHEETS](https://en.wikipedia.org/wiki/Google_Sheets)

### Frameworks, Libraries & Programs Used

1. [Git](https://git-scm.com/)
   - Git was used for version control by utilizing the Gitpod terminal to commit to Git and Push to GitHub.
1. [GitHub:](https://github.com/)
   - GitHub is used to store the projects code after being pushed from Git.
1. [Heroku:](https://www.heroku.com/)
   - Was used to host the game.
1. [Lucid:](https://www.lucidchart.com/)
   - Was used to make the logic flow chart in this readme.
1. [Balsamiq:](https://balsamiq.com/)
   - Was used to create the wireframe for the game.

## TESTING

### Testing User Stories from User Experience (UX) Section

- #### First Time Visitor Goals

  1. As a First Time Visitor, I want to understand clearly the game mechanics.
     1. When the game loads there are instructions on how to set up the game. 
     2. When the game loads there are instructions on how to use game commands and in particular there are 'help' and 'about' commands that give an even more detailed discription of how to play the game. 
     3. A legend is printed to describe the different symbols on the board.
  2. As a First Time Visitor, I want to understand the game controls.
     1. The 'about' command will describe the how the coordinates work.
     2. The introduction information and the 'help' command describe how to enter coordinates.
     3. Upon being prompted for input an example is given.
  3. As a First Time Visitor, I want to be able keep track of score.
     1. At the beginning of the game the top 5 best winning streaks are printed.
     2. Every time a shot is fired 'Hit' or 'Miss' is printed. 
     3. Each board has the number of hits taken displayed in each round.
     4. At the end of the game the results are recorded to the database.
     5. The user can type 'scores' at any time to see the top 5 best winning streaks from past users.

- #### Returning Visitor Goals

  1. As a Returning Visitor, see my previous scores and play again.
     1. At the beginning of the game the top 5 best winning streaks are printed.
     2. When the user logs in again their entire score history is printed.
     3. The user can type 'scores' at any time to see the top 5 best winning streaks from past users.
     4. At the end of the game the results are recorded to the database.

### Known Bugs

#### Solved Bugs

- Having split the code up into modules the run_game function needed to me accessible in helpers
  but importing run into helpers caused a circular import error.
    - I was able to export the function by creating a function that takes in a function as a parameter
    and saves it to a dictionary in the global scope of the helpers module.

#### Remaining Bugs

- No remaining bugs found

### Further Testing

- Tested locally and on the Code Institute Heroku terminal.
- Test giving the program invalid input; wrong characters, off board values, too many ships for board size, board size too big.
- Friends and family members were asked to review the site and documentation to point out any bugs and/or user experience issues.

### Validator Testing

  - PEP8
    All three files passed the PEP8 validator tests:
    
    **run.py**
    ![Run](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/run_pep8.png)
    **api_calls.py**
    ![API](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/api_pep8.png)
    **helpers.py**
    ![Helpers](https://github.com/RobTheThief/battleships-ci-3/blob/main/assets/media/helpers_pep8.png)


## Deployment

- Local deployment was achieved with with Python from the console. The game was developed on a Ubuntu OS and so was already installed. Steps are as follows:
  - Run `python3 run.py` in the terminal with root directory of the project.

- Heroku Deployment:
    - Create a new Heroku app.
    - Set the build packs to `Python` and `NodeJS` in that order.
    - Set Config Vars key value pairs for:
      1. `PORT`: `8000`
      1. `CREDS`: `{CREDS Object}` where {CREDS Object} is from the credentials file dowoloaded from Google Cloud Platform.
    - Enter `heroku login -i` command in the terminal with root directory of the project.
    - Enter Heroku username and password.
    - Enter `git push --set-upstream https://git.heroku.com/battleships-ci-3.git main` to deploy.
    - Enter `git push --set-upstream https://github.com/RobTheThief/battleships-ci-3.git main` to reset upstream to github.

The live link can be found here - https://battleships-ci-3.herokuapp.com/

## Credits
  
  The Code Institute Heroku console was used to deploy the game.

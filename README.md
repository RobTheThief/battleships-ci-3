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

  1. As a First Time Visitor, .....
     1. Solution
     2. Solution
     3. Solution
  2. As a First Time Visitor, ....
     1. Solution
     2. Solution
     3. Solution
  3. As a First Time Visitor, I want to be able.....
     1. Solution
     2. Solution
     3. Solution

- #### Returning Visitor Goals

  1. As a Returning Visitor, I want to find ....
     1. Solution
     2. Solution
     3. Solution
  2. As a Returning Visitor, I want to ....
      1. Solution
     2. Solution
     3. Solution
  3. As a Returning Visitor, I want to ....
     1. Solution
     2. Solution
     3. Solution

### Known Bugs

- Bug description
  - Solution if any:
  1. point
  2. point

### Further Testing

- The Website was tested on Google Chrome, Firefox, Microsoft Edge, Brave Browser, Ecosia and Safari.
- The website was viewed on a variety of devices such as Desktop, Laptop, Samsung S9, S10, iPhone X.
- Friends and family members were asked to review the site and documentation to point out any bugs and/or user experience issues.

### Validator Testing

- HTML
  - No errors were returned when passing through the official W3C validator.
    ![HTML VALIDATOR](https://link to screenshot)
- CSS
  - No errors were found when passing through the official(Jigsaw) validator.
    ![CSS VALIDATOR](https://link to screenshot)
- Accessibility

  - I confirm that the colours and fonts are easy to read and accessible by running it through the lighthouse in devtools.

  ![LIGHTHOUSE METRICS](https://link to screenshot)
  
  - JSHint

  - PEP8

## Deployment

- The site was deployed to GitHub pages. The steps to deploy are as follows:
  - In the GitHub repository, navigate to the Settings tab
  - From the source section drop-down menu, select the main branch.
  - Once the main branch has been selected, the page will be automatically refreshed with a detailed ribbon display to indicate the successful deployment.

The live link can be found here - https://link

- Local deployment was achieved with with Python from the console. The game was developed on a Ubuntu OS and so was already installed. Steps are as follows:
  - Run `python3 -m http.server` in the terminal with root directory of the project.
  - hold ctrl and click on the link provided in the terminal.
  - getting the ip adderss of the PC I was able to also access this server from my mobiles device.

- Heroku
    - Step 1
    - Step 2

The live link can be found here - https://link

## Credits
    Any help you had, tutorials, contriputions

### Content

- icons, code form other sources

### Media

- Photos [Source](https://link)
- Other photos [Source](https://link)
- Audio [Source](https://link)

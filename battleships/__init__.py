"""
    The Battleships package includes helpers, api_calls, and boards.
    Api calls using gspread and google-auth are made using api_calls.
    The baord class that creates the games boards for each player
    is found in boards.
    The rest of the game functions are found in helpers including
    run_game; the main game flow function.
    Sub packages include:
    math, time, os, pyfiglet, numpy, gspread, google-auth, copy,
    getpass
"""

from . import helpers
from . import api_calls
from . import boards

"""
    This module contains the functions and data necessary
    to make API calls to Google sheets to manage the
    database.
"""

import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ci-3-python')


def update_cell(cell, value, scores):
    """
        Updates cell on scores sheet
    """
    scores.update(cell, value)


def get_sheet_data():
    """
        Gets the spreadsheet and the cell data from the Google sheet
        and returns a list with the cell values and the scores sheet
    """
    scores = SHEET.worksheet('Scores')
    all_values = scores.get_all_values()
    return [all_values, scores]

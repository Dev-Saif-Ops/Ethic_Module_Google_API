import os
import sys
import git
repo_path = str(git.Repo('.', search_parent_directories=True).working_tree_dir)
sys.path.append(repo_path)
os.chdir(repo_path)

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from credentials.credential_manager import credential_management

def create(title):
  """
  Creates the Sheet the user has access to.
  Load pre-authorized user credentials from the environment.
  """
  creds = credential_management()
  # pylint: disable=maybe-no-member
  try:
    service = build("sheets", "v4", credentials=creds)
    spreadsheet = {"properties": {"title": title}}
    spreadsheet = (
        service.spreadsheets()
        .create(body=spreadsheet, fields="spreadsheetId")
        .execute()
    )
    print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
    return spreadsheet.get("spreadsheetId")
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error


if __name__ == "__main__":
  # Pass: title
  create("mysheet_1")

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

def create_sheets_service(credentials_file):
    # Load pre-authorized user credentials from the provided credentials file
    creds, _ = google.auth.load_credentials_from_file(credentials_file)
    
    # Create Sheets API service
    return build("sheets", "v4", credentials=creds)

def create_new_spreadsheet(sheets_service, title):
    # Create a new spreadsheet
    spreadsheet = {"properties": {"title": title}}
    spreadsheet = sheets_service.spreadsheets().create(body=spreadsheet, fields="spreadsheetId").execute()

    # Get the ID of the newly created spreadsheet
    spreadsheet_id = spreadsheet.get("spreadsheetId")
    print(f"New Spreadsheet ID: {spreadsheet_id}")
    return spreadsheet_id

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
  
def copy_data_to_spreadsheet(sheets_service, source_spreadsheet_id, destination_spreadsheet_id):
    # Get data from the source spreadsheet
    source_data = sheets_service.spreadsheets().values().get(spreadsheetId=source_spreadsheet_id, range="Sheet1").execute().get("values", [])

    # Write data to the destination spreadsheet
    body = {"values": source_data}
    sheets_service.spreadsheets().values().update(
        spreadsheetId=destination_spreadsheet_id,
        range="Sheet1",
        body=body,
        valueInputOption="RAW"
    ).execute()

if __name__ == "__main__":
    # Replace with the path to your credentials file
    CREDENTIALS_FILE = "Put_your_PATH"

    # Replace with the ID of the existing spreadsheet you want to copy
    source_spreadsheet_id = "Put_your_ID"

    # Replace with the title of the new spreadsheet
    new_spreadsheet_title = "cp_newsheet"

    # Create Sheets API service
    sheets_service = create_sheets_service(CREDENTIALS_FILE)

    # Create a new spreadsheet
    new_spreadsheet_id = create_new_spreadsheet(sheets_service, new_spreadsheet_title)

    # Copy data from the existing spreadsheet to the new spreadsheet
    copy_data_to_spreadsheet(sheets_service, source_spreadsheet_id, new_spreadsheet_id)
    print(f"Data copied from '{source_spreadsheet_id}' to '{new_spreadsheet_id}'")

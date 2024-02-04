import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import csv
import chardet

def csv_to_google_sheet(csv_file_path, spreadsheet_id, credentials_file):
    # Load pre-authorized user credentials from the provided credentials file
    creds, _ = google.auth.load_credentials_from_file(credentials_file)

    try:
        # Create Sheets API service
        service = build("sheets", "v4", credentials=creds)

        # Detect encoding
        with open(csv_file_path, "rb") as rawdata:
            result = chardet.detect(rawdata.read())
            encoding = result["encoding"]

        # Read data from CSV with detected encoding
        with open(csv_file_path, "r", encoding=encoding) as csv_file:
            csv_data = csv.reader(csv_file)
            values = list(csv_data)

        # Prepare the update request
        body = {"values": values}
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range="Sheet1",  # Adjust the sheet name and range as needed
            body=body,
            valueInputOption="RAW"
        ).execute()

        print(f"Data from {csv_file_path} successfully uploaded to Google Sheet with ID {spreadsheet_id}")

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    # Replace with your actual Google Sheet ID
    SPREADSHEET_ID = "1t8LvOFqHdCqmRPaavK1rF38ZHBu1IgkS3GsqSYqZ6gY"
    # Replace with the path to your local CSV file
    CSV_FILE_PATH = "/home/hi-tech/ModuleGoogleAPI/csvs/Sample-Spreadsheet-50000-rows.csv"
    # Replace with the path to your credentials file
    CREDENTIALS_FILE = "/home/hi-tech/ModuleGoogleAPI/credentials/service_credentials.json"

    csv_to_google_sheet(CSV_FILE_PATH, SPREADSHEET_ID, CREDENTIALS_FILE)

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_service_account():
    creds_path = os.getenv("CREDS_PATH")
    if not creds_path:
        raise EnvironmentError("Environment variable CREDS_PATH not set.")
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def list_drive_files():
    service = authenticate_service_account()

    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)"
    ).execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['id']})")

if __name__ == '__main__':
    list_drive_files()

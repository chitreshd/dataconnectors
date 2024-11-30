import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from termcolor import colored

# Scopes required for accessing Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def authenticate():
    """
    Authenticate the user and return the Google Drive service object.
    """
    creds = None

    # Get the credentials file path from the environment variable
    creds_path = os.getenv("CREDS_PATH")
    if not creds_path:
        raise EnvironmentError("Environment variable CREDS_PATH not set.")

    # Token.json stores the user's access and refresh tokens
    token_path = "token.json"

    try:
        # Load credentials from token.json if it exists
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    except Exception:
        pass

    # If no valid credentials are available, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            flow.redirect_uri = "http://localhost:3030"
            print(flow.redirect_uri)
            print(flow.authorization_url())
            creds = flow.run_local_server(port=3030)

        # Save the credentials for future use
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    # Build the Drive API service object
    return build('drive', 'v3', credentials=creds)

def list_drive_files():
    """
    List files in the user's Google Drive.
    """
    try:
        service = authenticate()
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)"
        ).execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return

        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['id']})")


    except HttpError as error:
        print(f"An error occurred: {error}")

def get_file_permissions(file_id, service):
    """
    Retrieve permissions for a specific file or folder.
    """
    try:
        permissions = service.permissions().list(fileId=file_id, fields="permissions").execute()
        return permissions.get('permissions', [])
    except Exception as error:
        print(f"An error occurred while fetching permissions for file ID {file_id}: {error}")
        return []

def list_drive_files_and_permissions(service, parent_id=None, depth=0):
    """
    Recursively list files and their permissions in Google Drive.
    """
    query = f"'{parent_id}' in parents" if parent_id else "'root' in parents"
    results = service.files().list(
        q=query,
        pageSize=100,
        fields="nextPageToken, files(id, name, mimeType)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()
    items = results.get('files', [])

    if not items:
        print(colored(" " * depth + "No files found."), "red")
        return

    for item in items:
        mimeType = item['mimeType']
        type = 'File'
        color = 'green'
        if mimeType == 'application/vnd.google-apps.folder':
            type = 'Folder'
            color = 'yellow'

        text = (" " * depth + f"{type}: {item['name']} (ID: {item['id']}, Type: {item['mimeType']})")
        print(colored(text, color))

        # Fetch and print permissions
        permissions = get_file_permissions(item['id'], service)
        if not permissions:
            text = (" " * (depth + 2) + "No permissions found.")
            print(colored(text, "cyan", None, ["bold"]))
        else:
            text = (" " * (depth + 2) + "Permissions:")
            print(colored(text, "cyan", None, ["bold"]))
            for permission in permissions:
                text = (" " * (depth + 4) +
                        f"- Role: {permission.get('role')}, Type: {permission.get('type')}, Email: {permission.get('emailAddress', 'N/A')}")
                print(colored(text, "cyan"))

        # If the item is a folder, recurse into it
        if mimeType == 'application/vnd.google-apps.folder':
            list_drive_files_and_permissions(service, parent_id=item['id'], depth=depth + 2)

def main():
    service = authenticate()
    print("Listing files and permissions in Google Drive:")
    list_drive_files_and_permissions(service)

if __name__ == '__main__':
    main()

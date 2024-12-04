import os
import sqlite3
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from termcolor import colored

# Scopes required for accessing Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

# Connect to SQLite database
conn = sqlite3.connect("documents_users.db")
cursor = conn.cursor()

# Create tables
def create_tables():
    # Documents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_name TEXT NOT NULL,
            doc_id TEXT NOT NULL UNIQUE,
            doc_type TEXT NOT NULL,
            doc_size INTEGER DEFAULT 0,
            parent_id TEXT NOT NULL
        );
    """)

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER NOT NULL,
            user_email TEXT NOT NULL,
            user_role TEXT NOT NULL,
            user_type TEXT NOT NULL,
            FOREIGN KEY (doc_id) REFERENCES documents (id) ON DELETE CASCADE
        );
    """)

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS page_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_token INTEGER NOT NULL,
            drive
            doc_id INTEGER NOT NULL,
            user_email TEXT NOT NULL,
            user_role TEXT NOT NULL,
            user_type TEXT NOT NULL,
            FOREIGN KEY (doc_id) REFERENCES documents (id) ON DELETE CASCADE
        );
    """)
    conn.commit()

# Insert a document with associated users
def insert_document_by_doc_id(doc_name, doc_id, doc_type, doc_size, parent_id):
    try:

        #check if the doc exist
        cursor.execute("SELECT id FROM documents WHERE doc_id = ?", (doc_id,))
        existing_doc = cursor.fetchone()
        
        if existing_doc:
            #print("Document ",doc_name, "already exist");
            return existing_doc[0]

        # Insert the document
        cursor.execute("INSERT INTO documents (doc_name, doc_id, doc_type, doc_size, parent_id) VALUES (?,?,?,?,?)", 
                (doc_name, doc_id, doc_type, doc_size, parent_id))
        doc_row_id = cursor.lastrowid  # Get the document's row ID

        conn.commit()
        return doc_row_id
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        return None

# Insert associated users
def insert_users(doc_row_id, users):
    try:
        # Insert associated users

        cursor.executemany(
            "INSERT INTO users (doc_id, user_email, user_role, user_type) VALUES (?, ?, ?, ?)",
            [(doc_row_id, email, role, user_type) for email, role, user_type in users]
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")

# Retrieve users for a document by name, ID, or type
def get_users_by_document(identifier, identifier_type):
    query = """
        SELECT u.user_email, u.user_role, u.user_type
        FROM users u
        JOIN documents d ON u.doc_id = d.id
    """
    if identifier_type == "name":
        query += " WHERE d.doc_name = ?;"
    elif identifier_type == "id":
        query += " WHERE d.doc_id = ?;"
    elif identifier_type == "type":
        query += " WHERE d.doc_type = ?;"
    elif identifier_type == "size":
        query += " WHERE d.doc_size = ?;"
    elif identifier_type == "parent_id":
        query += " WHERE d.parent_id = ?;"
    else:
        raise ValueError("Invalid identifier_type. Use 'name', 'id', 'type', 'size', 'parent_id'.")
    
    cursor.execute(query, (identifier,))
    return cursor.fetchall()

# Add or update a user for a given document name
def add_or_update_user_by_doc_name(doc_name, user_email, user_role, user_type):
    # Find the document ID
    cursor.execute("SELECT id FROM documents WHERE doc_name = ?", (doc_name,))
    doc_row = cursor.fetchone()
    if doc_row:
        doc_id = doc_row[0]
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE doc_id = ? AND user_email = ?", (doc_id, user_email))
        user_row = cursor.fetchone()
        if user_row:
            # Update user details
            cursor.execute("UPDATE users SET user_role = ?, user_type = ? WHERE id = ?", 
                           (user_role, user_type, user_row[0]))
        else:
            # Insert new user
            cursor.execute("INSERT INTO users (doc_id, user_email, user_role, user_type) VALUES (?, ?, ?, ?)", 
                           (doc_id, user_email, user_role, user_type))
        conn.commit()
    else:
        print(f"Document with name '{doc_name}' not found.")

# Add or update a user for a given document name
def add_or_update_user_by_row_id(doc_row_id, user_email, user_role, user_type):
    # Check if user exists
    cursor.execute("SELECT id FROM users WHERE doc_id = ? AND user_email = ?", (doc_row_id, user_email))
    user_row = cursor.fetchone()
    if user_row:
        # Update user details
        cursor.execute("UPDATE users SET user_role = ?, user_type = ? WHERE id = ?", 
            (user_role, user_type, user_row[0]))
    else:
    # Insert new user
        cursor.execute("INSERT INTO users (doc_id, user_email, user_role, user_type) VALUES (?, ?, ?, ?)", 
            (doc_row_id, user_email, user_role, user_type))
    conn.commit()


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
            pageSize=10, fields="nextPageToken, files(id, name, size)"
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
        fields="nextPageToken, files(id, name, mimeType, size, description)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()
    items = results.get('files', [])

    if not items:
        #print(colored(" " * depth + "No files found."), "red")
        return

    for item in items:
        mimeType = item['mimeType']
        doc_type = 'File'
        color = 'green'
        if mimeType == 'application/vnd.google-apps.folder':
            doc_type = 'Folder'
            color = 'yellow'

        doc_name = item['name']
        doc_id = item['id']
        doc_size = int(item.get('size')) if item.get('size') else 0

        doc_row_id  = insert_document_by_doc_id(doc_name, doc_id, doc_type, doc_size, 
                parent_id if parent_id else 0)

        # Fetch and print permissions
        permissions = get_file_permissions(doc_id, service)
        if not permissions:
            text = (" " * depth + f"{doc_name} (ID: {doc_id}, {doc_type}, Permissions [N/A], {doc_size})")
            print(colored(text, color))
        else:
            permissions_len = str(len(permissions))

            text = (" " * depth + 
                    f"{doc_name} (ID: {doc_id}, {doc_type}, Permissions [{permissions_len}], {doc_size})")
            print(colored(text, color))
            for permission in permissions:

                user_email = permission.get('emailAddress', 'N/A')
                user_role = permission.get('role')
                user_type = permission.get('type')

                text = (" " * (depth + 4) + 
                        f" {user_email} [ {user_role}, {user_type}] ")
                print(colored(text, "cyan"))
                if doc_row_id:
                    add_or_update_user_by_row_id(doc_row_id, user_email, user_role, user_type)

        # If the item is a folder, recurse into it
        if mimeType == 'application/vnd.google-apps.folder':
            list_drive_files_and_permissions(service, parent_id=item['id'], depth=depth + 2)

def main():
    create_tables()

    service = authenticate()
    print("Listing files and permissions in Google Drive:")
    list_drive_files_and_permissions(service)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    main()

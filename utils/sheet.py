import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_credentials(auth_path, token_path):
    """
    This function automatically stores the user's access and refresh tokens
    after the first time user completes authorization.
    It needs to be deleted when SCOPE changes.
    """

    creds = None
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                auth_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_sheet():
    """
        helper function to get sheet object.
        returns: sheet(object)
    """
    service = build('sheets', 'v4', credentials=get_credentials('utils/creds/credentials.json',
                                                                'utils/creds/token.pickle'))
    sheet = service.spreadsheets()
    return sheet

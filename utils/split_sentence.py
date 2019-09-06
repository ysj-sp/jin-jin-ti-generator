# -*- coding: utf-8 -*-
"""Split input sentences on google spread sheet into list of words with NLP tools.

"""

import os
import sys
import pickle

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from ckiptagger import WS


def get_sheet():
  """ helper function to get sheet object.

  This function automatically stores the user's access and refresh tokens
  after the first time user completes authorization.
  It needs to be deleted when SCOPE changes.

  returns: sheet(object)
  """

  creds = None
  if os.path.exists('./creds/token.pickle'):
    with open('./creds/token.pickle', 'rb') as token:
      creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          './creds/credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('./creds/token.pickle', 'wb') as token:
      pickle.dump(creds, token)

  service = build('sheets', 'v4', credentials=creds)
  sheet = service.spreadsheets()
  return sheet


def main():
  # Call the Sheets API
  sheet = get_sheet()
  result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                              range=RANGE_NAME).execute()
  sentence_list = result.get('values', [])
  sentence_list = [str(s[0]) for s in sentence_list if len(s) == 1]

  if DEBUG:
    print(sentence_list)

  # # load pre-trained models
  ws = WS("./ckiptagger_models")

  word_sentence_list = ws(sentence_list)
  word_sentence_list = [[" ".join(words)] for words in word_sentence_list]

  if DEBUG:
    for words in word_sentence_list:
      print(words)
    input(len(word_sentence_list))

  # write back to spreadsheet.
  updated_range = "datasets!B2:B{}".format(len(word_sentence_list) + 1)
  value_input_option = 'RAW'
  value_range_body = {
      "majorDimension": "DIMENSION_UNSPECIFIED",
      "range": updated_range,
      "values": word_sentence_list
  }

  request = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=updated_range,
                                  valueInputOption=value_input_option, body=value_range_body)
  try:
    response = None
    response = request.execute()
  except HttpError as identifier:
    print("Don't forget to delete pickle when chaning scope")
    print(identifier)
  finally:
    if response is not None:
      print("OK")


if __name__ == '__main__':
  os.chdir(os.path.dirname(sys.argv[0]))
  DEBUG = False
  # If modifying these scopes, delete the file token.pickle.
  SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

  # The ID and range of a sample spreadsheet.
  SPREADSHEET_ID = '12HLFguNa2jFWDOFP5_UzaAjZ9u5NhPJhUQGr8193WIs'
  RANGE_NAME = 'datasets!A2:A'

  main()

# -*- coding: utf-8 -*-
"""Split input sentences on google spread sheet into list of words with NLP tools.

"""

import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER


def get_sheet():
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('./creds/token.pickle'):
    with open('./creds/token.pickle', 'rb') as token:
      creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          './creds/client_secret_947466489-4dqoeedailijsv9qji792ftg3d3q9k3u.apps.googleusercontent.com.json', SCOPES)
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
  sentence_list = [str(s[0]) for s in sentence_list]

  if DEBUG:
    print(sentence_list)

  # load pre-trained models
  ws = WS("./ckiptagger_models")
  pos = POS("./ckiptagger_models")
  ner = NER("./ckiptagger_models")

  word_sentence_list = ws(sentence_list)

  # recommend_dictionary = dictionary1, # words in this dictionary are encouraged
  # coerce_dictionary = dictionary2, # words in this dictionary are forced
  print(word_sentence_list)
  input("------------")
  # TODO: write back to spreadsheet.


if __name__ == '__main__':
  DEBUG = True
  # If modifying these scopes, delete the file token.pickle.
  SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

  # The ID and range of a sample spreadsheet.
  SPREADSHEET_ID = '12HLFguNa2jFWDOFP5_UzaAjZ9u5NhPJhUQGr8193WIs'
  RANGE_NAME = 'datasets!A2:A11'

  main()

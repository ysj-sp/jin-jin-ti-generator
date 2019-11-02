# -*- coding: utf-8 -*-
"""Split input sentences on google spread sheet into list of words with NLP tools.

"""

import os
import sys

from googleapiclient.errors import HttpError
from ckiptagger import WS
from .sheet import get_sheet


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

    request = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                                    range=updated_range,
                                    valueInputOption=value_input_option,
                                    body=value_range_body)
    try:
        response = None
        response = request.execute()
    except HttpError as identifier:
        print("Don't forget to delete pickle when changing scope")
        print(identifier)
    finally:
        if response is not None:
            print("OK")


if __name__ == '__main__':
    os.chdir(os.path.dirname(sys.argv[0]))
    DEBUG = False

    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = '12HLFguNa2jFWDOFP5_UzaAjZ9u5NhPJhUQGr8193WIs'
    RANGE_NAME = 'datasets!A2:A'

    main()

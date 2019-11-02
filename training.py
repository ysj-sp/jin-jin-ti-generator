import numpy as np

from utils.sheet import get_sheet
from tensorflow import keras


def get_sheet_data(sheet, sheet_id, sheet_range):
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=sheet_range).execute()
    sentence_list = result.get('values', [])
    sentence_list = [str(s[0]) for s in sentence_list if len(s) == 1]

    return sentence_list


def text_to_index(corpus, word2idx):
    new_corpus = []
    for doc in corpus:
        new_doc = []
        for word in doc:
            try:
                new_doc.append(word2idx[word])
            except KeyError:
                new_doc.append(0)
        new_corpus.append(new_doc)
    return np.array(new_corpus)


def translated_text_to_index(corpus):
    new_corpus = []
    for doc in corpus:
        new_doc = []
        for word in doc:
            if word == '*':
                new_doc.append(1)
            else:
                new_doc.append(0)
        new_corpus.append(new_doc)
    return np.array(new_corpus)


def new_model(embedding_layer):
    model = keras.Sequential()
    model.add(embedding_layer)
    # model.add(keras.layers.GRU(16))
    model.add(keras.layers.Bidirectional(keras.layers.LSTM(64)))
    model.add(keras.layers.Dense(100, activation='relu'))
    model.add(keras.layers.Dense(100, activation='relu'))
    model.add(keras.layers.Dense(20, activation='sigmoid'))

    model.compile(optimizer=keras.optimizers.Adam(1e-2),
                  loss='MSE',
                  metrics=['accuracy'])
    return model


def main():
    sheet = get_sheet()
    input_data = get_sheet_data(sheet, SPREADSHEET_ID, 'datasets!B2:B')
    label_data = get_sheet_data(sheet, SPREADSHEET_ID, 'datasets!C2:C')

    dim = 0
    word_vecs = {}
    with open('cna.cbow.512d.0.txt') as f:
        for line in f:
            tokens = line.strip().split()

            if len(tokens) == 2:
                dim = int(tokens[1])
                continue

            word = tokens[0]
            vec = np.array([float(t) for t in tokens[1:]])
            word_vecs[word] = vec

    embedding_matrix = np.zeros((len(word_vecs) + 1, dim))
    word2idx = {}

    for i, vocab in enumerate(word_vecs):
        embedding_matrix[i + 1] = word_vecs[vocab]
        word2idx[vocab] = i + 1

    embedding_layer = keras.layers.Embedding(input_dim=embedding_matrix.shape[0],
                                             output_dim=embedding_matrix.shape[1],
                                             weights=[embedding_matrix],
                                             trainable=False)
    X = text_to_index(input_data, word2idx)
    X = keras.preprocessing.sequence.pad_sequences(X, maxlen=20)

    Y = translated_text_to_index(label_data)
    Y = keras.preprocessing.sequence.pad_sequences(Y, maxlen=20)

    model = new_model(embedding_layer)
    model.summary()

    model.fit(x=X, y=Y, batch_size=300, epochs=100, validation_split=0.1)

    test_data = [['你', '的', '東西', '就是', '我', '的', '東西']]
    P = text_to_index(test_data, word2idx)
    P = keras.preprocessing.sequence.pad_sequences(P, maxlen=20)

    print(P)

    predict = model.predict(P)

    print(predict)


if __name__ == '__main__':
    DEBUG = False

    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = '12HLFguNa2jFWDOFP5_UzaAjZ9u5NhPJhUQGr8193WIs'
    RANGE_NAME = 'datasets!B2:B'

    main()

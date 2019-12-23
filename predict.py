import numpy as np

from training import text_to_index
from tensorflow import keras
from ckiptagger import WS
from googletrans import Translator


def get_should_translate_index(arr):
    """
        function to get index of words that need to be translated
        return: result(array)
    """
    result = []
    for i, item in enumerate(arr):
        if item > 0.25:
            result.append(i)

    return result


def get_prediction(line, word2idx, line_length):
    test_data = []
    test_data.append(line)

    # Load split sentence model
    ws = WS("./utils/data")
    split_line = ws(test_data)
    T = text_to_index(split_line, word2idx)
    T = keras.preprocessing.sequence.pad_sequences(T, maxlen=line_length)

    return split_line, T


def get_word_vector_data():
    word_vecs = {}
    with open('cna.cbow.512d.0.txt') as f:
        for line in f:
            tokens = line.strip().split()

            if len(tokens) == 2:
                continue

            word = tokens[0]
            vec = np.array([float(t) for t in tokens[1:]])
            word_vecs[word] = vec

    word2idx = {}

    for i, vocab in enumerate(word_vecs):
        word2idx[vocab] = i + 1

    return word_vecs, word2idx


def get_translated_line(line, should_translate_index, line_length):
    translator = Translator()

    for index in should_translate_index:
        target_index = index - line_length
        # Handle boundary
        if target_index < -(len(line)):
            continue
        # Translate target word
        translated_text = translator.translate(line[index - line_length], dest="en", src="zh-Tw").text
        line[index - line_length] = translated_text
    result = ' '.join(line)

    return result


def main():
    word_vecs, word2idx = get_word_vector_data()
    # Load trained model
    model = keras.models.load_model('saved_model/my_model')

    while 1:
        input_test_data = input("Enter your sentence with Chinese or exit to close application: ")

        # Close application if user type `exit`
        if input_test_data == 'exit':
            break

        split_line, T = get_prediction(input_test_data, word2idx, MAX_LEN)

        # Get prediction from trained model
        predict = model.predict(T)
        should_translate_index = get_should_translate_index(predict[0])

        translate_line = split_line[0].copy()
        prediction = get_translated_line(translate_line, should_translate_index, MAX_LEN)

        print(split_line[0], prediction)


if __name__ == '__main__':
    DEBUG = False
    MAX_LEN = 20

    main()

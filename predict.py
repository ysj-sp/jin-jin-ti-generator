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


def main():
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

    # Load trained model
    model = keras.models.load_model('saved_model/my_model')

    while 1:
        test_data = []

        input_test_data = input("Enter your sentence with Chinese or exit to close application: ")

        # Close application if user type `exit`
        if input_test_data == 'exit':
            break

        test_data.append(input_test_data)

        # Load split sentence model
        ws = WS("./utils/data")
        split_test_data = ws(test_data)

        T = text_to_index(split_test_data, word2idx)
        T = keras.preprocessing.sequence.pad_sequences(T, maxlen=MAX_LEN)

        # Get prediction from trained model
        predict = model.predict(T)
        should_translate_index = get_should_translate_index(predict[0])

        translate_line = split_test_data[0].copy()
        translator = Translator()

        for index in should_translate_index:
            target_index = index - MAX_LEN

            # Handle boundary
            if target_index < -(len(translate_line)):
                continue

            # Translate target word
            translated_text = translator.translate(translate_line[index - MAX_LEN], dest="en", src="zh-Tw").text
            translate_line[index - MAX_LEN] = translated_text

        result = ' '.join(translate_line)
        print(split_test_data[0], result)


if __name__ == '__main__':
    DEBUG = False
    MAX_LEN = 20

    main()

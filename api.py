from flask import Flask, request, jsonify
from predict import get_word_vector_data, get_should_translate_index, get_prediction, get_translated_line
from tensorflow import keras, Session, get_default_graph
from tensorflow.python.keras.backend import set_session

word_vecs, word2idx = get_word_vector_data()
sess = Session()
graph = get_default_graph()
set_session(sess)
model = keras.models.load_model('saved_model/my_model')

app = Flask(__name__)


@app.route('/predict', methods=['GET'])
def response():
    line = request.args.get('line', None)

    split_line, T = get_prediction(line, word2idx, MAX_LEN)

    global graph
    with graph.as_default():
        set_session(sess)
        predict = model.predict(T)

    should_translate_index = get_should_translate_index(predict[0])

    translate_line = split_line[0].copy()
    prediction = get_translated_line(translate_line, should_translate_index, MAX_LEN)

    response = {}

    if not line:
        response['Error'] = 'No line found, please send a line.'
    else:
        response['Message'] = prediction

    return jsonify(response)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    MAX_LEN = 20
    app.run(threaded=True, port=5000)

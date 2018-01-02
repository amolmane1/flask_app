from flask import Flask, redirect, url_for, request, jsonify
import json
from sklearn.externals import joblib

from .transformer import Transformer
from .predict import predict


app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        incoming_data = request.get_json()
        model, feature_names, predictor = get_model_and_feature_names_and_predictor()
        x, prediction_date = Transformer(incoming_data, feature_names, predictor).run()
        if x is not None:
            prediction_dict = predict(x, model)
            if prediction_dict is not None:
                prediction_dict['date'] = prediction_date
                return jsonify(prediction_dict)
        return jsonify(None)


def get_model_and_feature_names_and_predictor():
    with open('files/predictor.json', 'r') as f:
        predictor = json.load(f)
    with open('files/feature_names.json', 'r') as f:
        feature_names = json.load(f)
    model = joblib.load('files/model.pkl')
    return model, feature_names, predictor


if __name__ == '__main__':
    app.run(host='0.0.0.0')

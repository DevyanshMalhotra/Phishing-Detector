from flask import Flask
from flask_cors import CORS
import pickle
from flask import request, jsonify

from extract_features import extract_features

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

# Load the saved model
with open('svm_model_2.pickle', 'rb') as f:
    clf = pickle.load(f)


@app.route('/predict')
def predict():
    # Extract URL from request
    url = request.args.get('url')
    if url.startswith('https://www.google.com') or 'localhost' in url or 'phishtank' in url or '127.0.0.1' in url:
        return jsonify({
            'prediction': str(1)
        })
    else:
        # Extract features from URL
        features = extract_features(url)

        # Make prediction using SVM model
        prediction = clf.predict([features])[0]

        return jsonify({
            'prediction': str(prediction)
        })


if __name__ == '__main__':
    app.run(debug=True,  port=80)

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Load trained model and scaler
model = joblib.load('models/pop_model.joblib')
scaler = joblib.load('models/scaler.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    year = int(data.get('year', 2011))

    # Scale and reshape
    X = np.array([[year]])
    X_scaled = scaler.transform(X)

    # Predict multi-output
    preds = model.predict(X_scaled)[0]
    keys = ['total', 'male', 'female', 'urban', 'rural', 'under18']
    metrics = {k: int(v) for k, v in zip(keys, preds)}

    return jsonify({'metrics': metrics})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load models and encoder
yield_model = joblib.load('yield_model.pkl')
price_model = joblib.load('price_model.pkl')
encoder = joblib.load('encoder.pkl')  # Ensure this is the same encoder used during training

# Columns expected by the model (this should be consistent with training)
expected_columns = [
    'Soil Type', 'Weather Conditions', 'Irrigation Type_Drip', 
    'Irrigation Type_Flood', 'Irrigation Type_Sprinkler', 
    'Nutrients Level_High', 'Nutrients Level_Low', 'Nutrients Level_Medium',
    'Cancer Prevention Study Findings'
]

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Convert the data into a DataFrame
    user_input = pd.DataFrame(data, index=[0])

    # Add missing columns with default values
    for col in expected_columns:
        if col not in user_input.columns:
            user_input[col] = 0  # Assign 0 for missing categorical columns
    
    # Apply the encoder to transform the input data
    user_input_encoded = encoder.transform(user_input).toarray()
    
    # Make predictions
    yield_pred = yield_model.predict(user_input_encoded)[0]
    price_pred = price_model.predict(user_input_encoded)[0]

    return jsonify({
        'predicted_yield': yield_pred,
        'predicted_price': price_pred
    })

if __name__ == '__main__':
    app.run(debug=True)

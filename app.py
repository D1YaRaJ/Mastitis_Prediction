from flask import Flask, request, jsonify, render_template,send_from_directory
from flask_cors import CORS
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os

app = Flask(__name__)
CORS(app)

# Load the dataset
dataframe = pd.read_csv('dataset_95.csv')
data=dataframe.drop_duplicates( keep=False)

# Define features and target
X = data[['Temperature', 'Hardness', 'Pain', 'Milk Yield', 'Milk Color']]
y = data['Mastitis']

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        temperature = data['temperature']
        hardness = data['hardness']
        pain = data['pain']
        milk_yield = data['milk_visibility']
        milk_color = data['milk_color']

        # Prepare input data for prediction
        input_data = pd.DataFrame([[temperature, hardness, pain, milk_yield, milk_color]],
                                  columns=['Temperature', 'Hardness', 'Pain', 'Milk Yield', 'Milk Color'])

        # Make prediction
        prediction = model.predict(input_data)[0]
        result = {
            'prediction': "Mastitis Detected" if prediction == 1 else "No Mastitis"
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
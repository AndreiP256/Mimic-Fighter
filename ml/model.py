from sklearn.ensemble import RandomForestClassifier
from ml.data_collection import preprocess_data, scaler

# Initialize the model
model = RandomForestClassifier(n_estimators=100, random_state=42)

def train_model(data):
    print("Fitting model")
    X, y = preprocess_data(data)
    scaler.fit(X)  # Fit the scaler with the training data
    model.fit(X, y)

def predict_output(example_data):
    example_data_scaled = scaler.transform([example_data])
    predicted_output = model.predict(example_data_scaled)
    return predicted_output
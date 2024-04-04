import joblib
import numpy as np
from fastapi import FastAPI
from sklearn.datasets import load_iris

# Load the iris dataset
iris = load_iris()
# Initialize FastAPI app
app = FastAPI()

# Load the trained model
# model = joblib.load('model/model.joblib')

# Load the trained model in Docker
model = joblib.load("model.joblib")


# new idaa
# Define FastAPI endpoints
@app.get("/")
async def read_root():
    return {"message": "Welcome to the model API!"}


@app.post("/predict/")
async def predict_species(data: dict):
    # Implement your prediction logic here using the loaded model
    features = np.array(data["features"]).reshape(1, -1)
    prediction = model.predict(features)
    class_name = iris.target_names[prediction][0]
    return {"class": class_name}

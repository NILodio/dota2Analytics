import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = load_iris()
X, y = data.data, data.target

# Train model
model = RandomForestClassifier()
model.fit(X, y)


joblib.dump(model, "my_project/app/model/model.joblib")

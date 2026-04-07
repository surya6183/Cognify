import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("data/behavioral_dataset.csv")

X = df.drop("label", axis=1)
y = df["label"]

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=8,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "models/cognitive_model.pkl")

print("Model trained and saved successfully")
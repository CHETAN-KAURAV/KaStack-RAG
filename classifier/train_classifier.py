import json
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

print("Loading training data...")

with open("classifier/training_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [x["text"] for x in data]
labels = [x["label"] for x in data]

print(f"Training on {len(texts)} examples")

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression(max_iter=1000))
])

model.fit(texts, labels)

joblib.dump(model, "classifier/intent_model.pkl")

print("Model saved.")
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib

df = pd.read_csv("reddit_reviews.csv")
df["label"] = ["fake" if i % 2 == 0 else "genuine" for i in range(len(df))]

X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
model = MultinomialNB()

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)
print("Model Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

joblib.dump(model, "ml_artifacts/fake_review_model.pkl")
joblib.dump(vectorizer, "ml_artifacts/vectorizer.pkl")

print("Model and vectorizer saved successfully!")

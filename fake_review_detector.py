import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

print(" Loading Reddit review data...")

data = pd.read_csv('reddit_reviews.csv')

print("Columns found:", list(data.columns))

data.rename(columns={'text': 'review'}, inplace=True)

data = data.dropna(subset=['review'])
data = data[data['review'].str.strip() != ""]

def label_review(row):
    text = str(row['review']).lower()
    score = row['score']

    if any(word in text for word in ["amazing", "best ever", "unbelievable", "perfect", "superb", "worst", "awful", "terrible", "scam"]):
        return "fake"

    if len(text.split()) < 3:
        return "fake"

    if score < 2 and any(word in text for word in ["good", "great", "love", "nice"]):
        return "fake"

    return "genuine"

data['label'] = data.apply(label_review, axis=1)

print(f"Loaded {len(data)} reviews for training.")

X_train, X_test, y_train, y_test = train_test_split(
    data['review'], data['label'], test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer(stop_words='english', max_features=3000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = MultinomialNB()
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)
print("\n Model Performance:")
print("Accuracy:", round(accuracy_score(y_test, y_pred) * 100, 2), "%")
print("\nClassification Report:\n", classification_report(y_test, y_pred))

print("\n Try your own review below:")
while True:
    text = input("Enter a review (or type 'exit' to quit): ")
    if text.lower() == "exit":
        print(" Exiting fake review detector.")
        break
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    print(f" This review is likely: {prediction.upper()}")

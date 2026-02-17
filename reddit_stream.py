import praw
import pandas as pd
import joblib
import time
model = joblib.load("fake_review_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

reddit = praw.Reddit(
    client_id="n5w4bKMCt-Soay4D02jy6Q",
    client_secret="CMEAG14jje5CSy7ZouhptKUlKbPkCw",
    user_agent="FakeReviewApp (by u/DoughnutDry9693)",
    username="DoughnutDry9693",
    password="sai065##"
)
subreddit_name = "Android"
keyword = "vivo V60 review"
subreddit = reddit.subreddit(subreddit_name)
print(f" Listening for live comments in r/{subreddit_name} mentioning '{keyword}' ...")
while True:
    try:
        for comment in subreddit.stream.comments(skip_existing=True):
            if keyword.lower() in comment.body.lower():
                review_text = comment.body
                X = vectorizer.transform([review_text])
                prediction = model.predict(X)[0]
                label = "Fake" if prediction == "fake" else "Genuine"

                data = {
                    "author": comment.author.name if comment.author else "Unknown",
                    "text": review_text,
                    "predicted_label": label,
                    "created_utc": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
                }
                df = pd.DataFrame([data])
                df.to_csv("live_reviews.csv", mode="a", header=not pd.io.common.file_exists("live_reviews.csv"), index=False)
                print(f" New comment classified as {label}: {review_text[:80]}...")
    except Exception as e:
        print(f" Error: {e}")
        time.sleep(10)

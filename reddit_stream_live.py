import praw
import pandas as pd
import time

reddit = praw.Reddit(
    client_id="n5w4bKMCt-Soay4D02jy6Q",
    client_secret="CMEAG14jje5CSy7ZouhptKUlKbPkCw",
    user_agent="FakeReviewApp (by u/DoughnutDry9693)",
    username="DoughnutDry9693",
    password="sai065##"
)

TARGET_SUBREDDIT = "Android"  


CSV_FILE = "reddit_reviews.csv"

print(f" Streaming live comments from r/{TARGET_SUBREDDIT} ...")
comments_collected = []

while True:
    try:
        subreddit = reddit.subreddit(TARGET_SUBREDDIT)
        for comment in subreddit.stream.comments(skip_existing=True):
            text = comment.body
            author = str(comment.author)
            score = comment.score
            comments_collected.append([author, text, score])
            df = pd.DataFrame(comments_collected, columns=["author", "text", "score"])
            df.to_csv(CSV_FILE, index=False)

            print(f" New comment from {author} | Score: {score}")
            print(f" Text: {text[:80]}...\n")
            time.sleep(1)

    except Exception as e:
        print(" Error:", e)
        print("Reconnecting in 5 seconds...")
        time.sleep(5)

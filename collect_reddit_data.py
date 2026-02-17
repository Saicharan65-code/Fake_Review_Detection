import praw
import pandas as pd

reddit = praw.Reddit(
    client_id="n5w4bKMCt-Soay4D02jy6Q",
    client_secret="CMEAG14jje5CSy7ZouhptKUlKbPkCw",
    user_agent="FakeReviewApp (by u/DoughnutDry9693)",
    username="DoughnutDry9693",
    password="sai065##"
)

subreddit_name = "Android"
subreddit = reddit.subreddit(subreddit_name)

print(f"Collecting comments from r/{subreddit_name} ...")

comments = []
for comment in subreddit.comments(limit=200):
    comments.append({
        "author": str(comment.author),
        "text": comment.body,
        "score": comment.score
    })

df = pd.DataFrame(comments)
df.to_csv("reddit_reviews.csv", index=False)

print(" Data collected and saved as 'reddit_reviews.csv'")

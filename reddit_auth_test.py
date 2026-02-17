import praw

# Reddit API connection
reddit = praw.Reddit(
    client_id="n5w4bKMCt-Soay4D02jy6Q",
    client_secret="CMEAG14jje5CSy7ZouhptKUlKbPkCw",
    user_agent="FakeReviewApp (by u/DoughnutDry9693)",
    username="DoughnutDry9693",
    password="sai065##"  
)

try:
    print("🔄 Authenticating with Reddit...")
    print("✅ Logged in as:", reddit.user.me())
except Exception as e:
    print("❌ Login failed:", e)

KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092'] # Default for local testing, can be overridden by env
KAFKA_TOPIC = 'reddit_reviews'

MODEL_PATH = 'ml_artifacts/fake_review_model.pkl'
VECTORIZER_PATH = 'ml_artifacts/vectorizer.pkl'

POSTGRES_USER = 'user'
POSTGRES_PASSWORD = 'password'
POSTGRES_DB = 'review_db'
POSTGRES_HOST = 'localhost' # Default for local testing
POSTGRES_PORT = 5432

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

DETECTOR_HOST = 'localhost'
DETECTOR_PORT = 8000
DETECTOR_API_URL = f"http://{DETECTOR_HOST}:{DETECTOR_PORT}"

# Reddit API Credentials
REDDIT_CLIENT_ID = "n5w4bKMCt-Soay4D02jy6Q"
REDDIT_CLIENT_SECRET = "CMEAG14jje5CSy7ZouhptKUlKbPkCw"
REDDIT_USER_AGENT = "FakeReviewApp (by u/DoughnutDry9693)"
REDDIT_USERNAME = "DoughnutDry9693"
REDDIT_PASSWORD = "sai065##"

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_PATH = 'logs'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

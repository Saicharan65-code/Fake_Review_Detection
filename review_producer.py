from kafka import KafkaProducer
import praw
import json
import time
from datetime import datetime
import logging
import config
from utils.logger import setup_logger

# Setup logging
logger = setup_logger('producer')

class RedditStreamProducer:
    def __init__(self):
        """Initialize Reddit API and Kafka producer"""
        self.setup_reddit_client()
        self.setup_kafka_producer()
        
    def setup_reddit_client(self):
        """Setup Reddit API client"""
        try:
            self.reddit = praw.Reddit(
                client_id=config.REDDIT_CLIENT_ID,
                client_secret=config.REDDIT_CLIENT_SECRET,
                user_agent=config.REDDIT_USER_AGENT,
                username=config.REDDIT_USERNAME,
                password=config.REDDIT_PASSWORD
            )
            logger.info("Reddit client setup successful")
        except Exception as e:
            logger.error(f"Failed to setup Reddit client: {str(e)}")
            raise

    def setup_kafka_producer(self):
        """Setup Kafka producer with error handling and retries"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks='all',
                retries=3,
                retry_backoff_ms=1000
            )
            logger.info("Kafka producer setup successful")
        except Exception as e:
            logger.error(f"Failed to setup Kafka producer: {str(e)}")
            raise

    def format_comment(self, comment):
        """Format Reddit comment into structured data"""
        return {
            'comment_id': comment.id,
            'author': comment.author.name if comment.author else 'Unknown',
            'text': comment.body,
            'subreddit': comment.subreddit.display_name,
            'score': comment.score,
            'created_utc': datetime.fromtimestamp(comment.created_utc).isoformat(),
            'processed_at': datetime.now().isoformat()
        }

    def stream_comments(self, subreddit_name, keyword):
        """Stream comments from Reddit and produce to Kafka"""
        subreddit = self.reddit.subreddit(subreddit_name)
        logger.info(f"Starting to stream comments from r/{subreddit_name}")

        while True:
            try:
                for comment in subreddit.stream.comments(skip_existing=True):
                    if keyword.lower() in comment.body.lower():
                        # Format comment data
                        comment_data = self.format_comment(comment)
                        
                        # Send to Kafka
                        self.producer.send(
                            topic=config.KAFKA_TOPIC,
                            value=comment_data,
                            key=comment.id.encode('utf-8')
                        )
                        logger.info(f"Produced comment {comment.id} to Kafka")

            except Exception as e:
                logger.error(f"Error in comment stream: {str(e)}")
                time.sleep(10)  # Wait before retrying

    def close(self):
        """Clean up resources"""
        if self.producer:
            self.producer.flush()
            self.producer.close()
            logger.info("Kafka producer closed")

if __name__ == "__main__":
    producer = RedditStreamProducer()
    try:
        producer.stream_comments("Android", "vivo V60 review")
    except KeyboardInterrupt:
        logger.info("Shutting down producer")
        producer.close()
# dashboard_consumer.py (UPDATED)

from kafka import KafkaConsumer
import json
import pandas as pd
from datetime import datetime
import logging
import requests # <--- New import
from sqlalchemy import create_engine
import config
from utils.logger import setup_logger

# Setup logging
logger = setup_logger('consumer')

class ReviewProcessor:
    def __init__(self):
        """Initialize the review processor with database connection and API URL"""
        self.DETECTOR_API_URL = config.DETECTOR_API_URL + "/predict" # <--- New setup
        self.setup_database()
        self.setup_kafka_consumer()
        logger.info(f"Using Detector API at: {self.DETECTOR_API_URL}")


    def setup_model(self):
        """No longer needed - Model loaded by the separate API service"""
        # Remove all original contents of this method. 
        # (Keeping it as a placeholder to show the removal if necessary)
        pass 

    def setup_database(self):
        """Setup database connection"""
        try:
            self.engine = create_engine(config.DATABASE_URL)
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise

    def setup_kafka_consumer(self):
        """Setup Kafka consumer with error handling"""
        try:
            self.consumer = KafkaConsumer(
                config.KAFKA_TOPIC,
                bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                auto_offset_reset='latest',
                enable_auto_commit=False,
                group_id='review_processor_group'
            )
            logger.info("Kafka consumer setup successful")
        except Exception as e:
            logger.error(f"Failed to setup Kafka consumer: {str(e)}")
            raise

    def predict_review(self, text):
        """Classify review by calling the external API"""
        try:
            response = requests.post(self.DETECTOR_API_URL, json={"text": text}, timeout=5)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            
            result = response.json()
            if result.get('success'):
                return result['prediction']
            else:
                logger.error(f"API returned unsuccessful result: {result.get('error')}")
                return "API_Error"

        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP/API call error: {str(e)}")
            return "Connection_Error"
        except Exception as e:
            logger.error(f"Unexpected prediction error: {str(e)}")
            return "Unknown"

    def save_to_database(self, processed_data):
        """Save processed data to database"""
        try:
            df = pd.DataFrame([processed_data])
            df.to_sql('reviews', self.engine, if_exists='append', index=False)
            logger.info(f"Saved review {processed_data['comment_id']} to database")
        except Exception as e:
            logger.error(f"Database error: {str(e)}")

    def process_reviews(self):
        """Main processing loop"""
        logger.info("Starting review processing")
        
        try:
            for message in self.consumer:
                data = message.value
                
                # Enrich data with prediction
                # Note: 'text' is assumed to be the key containing the review text
                processed_data = {
                    **data,
                    'predicted_label': self.predict_review(data['text']), # Use text from incoming data
                    'processed_timestamp': datetime.now().isoformat()
                }

                # Save to database
                self.save_to_database(processed_data)

                # Commit offset
                self.consumer.commit()

        except KeyboardInterrupt:
            logger.info("Shutting down consumer")
            self.close()
        except Exception as e:
            logger.error(f"Processing error: {str(e)}")

    def close(self):
        """Clean up resources"""
        if self.consumer:
            self.consumer.close()
            logger.info("Kafka consumer closed")

if __name__ == "__main__":
    # Ensure you've removed the self.setup_model() call from __init__ if you update in place.
    processor = ReviewProcessor()
    processor.process_reviews()
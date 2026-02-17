# Reddit Review Analysis Pipeline

A data engineering pipeline for streaming and analyzing Reddit reviews using Kafka, ML, and real-time dashboard.

## Project Structure

```
capstone/
├── config/              # Configuration files
│   ├── config.py       # Main configuration
│   └── docker-compose.yml  # Docker services configuration
│
├── src/                # Source code
│   ├── data/          # Data storage
│   │   └── reddit_reviews.csv
│   │
│   ├── models/        # ML models and artifacts
│   │   ├── fake_review_detector.py
│   │   └── vectorizer.pkl
│   │
│   ├── pipeline/      # Data pipeline components
│   │   ├── review_producer.py   # Kafka producer
│   │   └── dashboard_consumer.py # Kafka consumer
│   │
│   ├── dashboard/     # Streamlit dashboard
│   │   └── app.py
│   │
│   └── utils/         # Utility functions
│       └── logger.py
│
├── logs/              # Application logs
├── tests/             # Unit tests
├── requirements.txt   # Project dependencies
└── README.md         # Project documentation
```

## Setup and Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the infrastructure:
```bash
docker-compose -f config/docker-compose.yml up -d
```

3. Run the pipeline:
```bash
# Start the producer
python src/pipeline/review_producer.py

# Start the consumer
python src/pipeline/dashboard_consumer.py

# Launch the dashboard
streamlit run src/dashboard/app.py
```

## Components

1. **Data Ingestion**: Streams Reddit comments in real-time
2. **Stream Processing**: Uses Kafka for reliable message processing
3. **ML Pipeline**: Analyzes reviews using trained models
4. **Storage**: Persists data in PostgreSQL
5. **Dashboard**: Real-time visualization with Streamlit
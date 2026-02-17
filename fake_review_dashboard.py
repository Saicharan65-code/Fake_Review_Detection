# fake_review_dashboard.py

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import time
import config # Assuming this contains your DATABASE_URL

# --- Configuration ---
DATABASE_URL = config.DATABASE_URL
REFRESH_RATE_SECONDS = 5

# --- Database Connection and Query ---
@st.cache_resource
def get_db_engine():
    """Create and cache the database engine."""
    try:
        engine = create_engine(DATABASE_URL)
        st.toast("✅ Database connection established.", icon='🔍')
        return engine
    except Exception as e:
        st.error(f"❌ Error connecting to database: {e}")
        return None

def fetch_data(engine):
    """Fetch the latest data and key metrics from the 'reviews' table."""
    if engine is None:
        return pd.DataFrame(), 0, 0, 0

    # 1. Fetch Key Metrics (Total, Fake, Genuine counts)
    metrics_query = text("""
        SELECT 
            COUNT(*) AS total_count,
            COUNT(CASE WHEN predicted_label = 'Fake' THEN 1 END) AS fake_count,
            COUNT(CASE WHEN predicted_label = 'Genuine' THEN 1 END) AS genuine_count
        FROM reviews
    """)

    # 2. Fetch Latest Reviews (for display table)
    latest_reviews_query = text("""
        SELECT 
            subreddit, 
            author, 
            score, 
            text, 
            predicted_label, 
            processed_timestamp 
        FROM reviews
        ORDER BY processed_timestamp DESC 
        LIMIT 20
    """)
    
    try:
        with engine.connect() as connection:
            # Execute metrics query
            metrics_result = pd.read_sql(metrics_query, connection).iloc[0]
            
            total_count = metrics_result['total_count']
            fake_count = metrics_result['fake_count']
            genuine_count = metrics_result['genuine_count']
            
            # Execute latest reviews query
            latest_reviews_df = pd.read_sql(latest_reviews_query, connection)
            latest_reviews_df['processed_timestamp'] = pd.to_datetime(latest_reviews_df['processed_timestamp']).dt.strftime('%H:%M:%S')

            return latest_reviews_df, total_count, fake_count, genuine_count

    except Exception as e:
        st.error(f"❌ Error fetching data: {e}. Ensure the 'reviews' table exists.")
        return pd.DataFrame(), 0, 0, 0

# --- Streamlit App Layout ---

st.set_page_config(
    page_title="Real-Time Fake Review Detector",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🚨 Real-Time Reddit Fake Review Detection Dashboard")
st.markdown("Monitoring live comments, classifying them using the ML model, and visualizing results.")

# --- Real-Time Loop ---
placeholder = st.empty()
engine = get_db_engine()

if engine:
    while True:
        # Fetch data inside the loop
        reviews_df, total, fake, genuine = fetch_data(engine)
        
        # Use placeholder to update the content dynamically
        with placeholder.container():
            
            # 1. Key Metrics Section
            st.header("📈 Key Performance Indicators (KPIs)")
            col1, col2, col3, col4 = st.columns(4)

            # Calculate percentages
            fake_percent = (fake / total * 100) if total > 0 else 0
            
            col1.metric("Total Reviews Processed", f"{total:,}")
            col2.metric("Fake Reviews Detected", f"{fake:,}", delta=f"{fake_percent:.1f}% of Total")
            col3.metric("Genuine Reviews", f"{genuine:,}")
            
            # Simple status indicator
            if fake_percent > 10:
                status_icon = "🔥 High Alert"
            elif fake_percent > 3:
                status_icon = "⚠️ Moderate"
            else:
                status_icon = "✅ Low Activity"
            
            col4.metric("Current Fake Rate Status", status_icon)

            st.divider()
            
            # 2. Latest Reviews Table
            st.header("Recent Classifications")
            
            # Highlight rows where prediction is 'Fake'
            def highlight_fake(s):
                return ['background-color: #ffcccc' if s['predicted_label'] == 'Fake' else '' for v in s]
            
            if not reviews_df.empty:
                st.dataframe(
                    reviews_df.style.apply(highlight_fake, axis=1), 
                    use_container_width=True, 
                    hide_index=True,
                    column_order=("processed_timestamp", "predicted_label", "subreddit", "text", "author", "score"),
                    column_config={
                        "text": st.column_config.TextColumn("Review Text", width="large"),
                        "predicted_label": st.column_config.TextColumn("Prediction", width="small"),
                        "processed_timestamp": st.column_config.TimeColumn("Time", format="HH:mm:ss")
                    }
                )
            else:
                st.info("Waiting for data... Ensure Kafka Producer and Consumer are running.")


        # Wait before refreshing the dashboard
        time.sleep(REFRESH_RATE_SECONDS)

else:
    st.warning("Cannot start dashboard without a database connection. Please check your 'config.py' and database service.")
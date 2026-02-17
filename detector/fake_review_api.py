# fake_review_api.py

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import config
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI Setup ---
app = FastAPI(
    title="Fake Review Detector API",
    description="Microservice for real-time fake/genuine review classification."
)

# --- Pydantic Schema for Request Body ---
class ReviewText(BaseModel):
    text: str

# --- Model Loading ---
model = None
vectorizer = None

def load_model_artifacts():
    """Load the trained model and vectorizer at startup."""
    global model, vectorizer
    try:
        # NOTE: Ensure MODEL_PATH and VECTORIZER_PATH are correct in config.py
        # and that the .pkl files are available to this service's volume.
        model = joblib.load(config.MODEL_PATH)
        vectorizer = joblib.load(config.VECTORIZER_PATH)
        logger.info("ML Model and Vectorizer loaded successfully.")
    except Exception as e:
        logger.error(f"FATAL: Failed to load model artifacts. Check paths/volumes. Error: {e}")
        # You might want to raise an exception to stop the service if the model is crucial.

load_model_artifacts()

# --- API Endpoints ---

@app.get("/")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "message": "Detector API is running"}

@app.post("/predict")
def predict_review(review: ReviewText):
    """
    Accepts review text and returns the fake/genuine classification.
    """
    if not model or not vectorizer:
        return {"error": "Model not loaded. Check server logs."}, 500

    text = review.text
    
    try:
        # Transform the text using the loaded vectorizer
        X = vectorizer.transform([text])
        
        # Get the prediction from the model
        prediction = model.predict(X)[0]
        
        # Map the internal label ("fake"/"genuine") to the output label
        result_label = "Fake" if prediction == "fake" else "Genuine"
        
        return {
            "text": text,
            "prediction": result_label,
            "success": True
        }
    except Exception as e:
        logger.error(f"Prediction processing error for text '{text}': {e}")
        return {"error": f"Prediction failed: {e}", "success": False}, 500
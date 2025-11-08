import opensmile
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib
import os

def analyze_sentiment(audio_path: str):
    """
    Analyze sentiment directly from an audio file using OpenSMILE feature extraction.
    
    Parameters
    ----------
    audio_path : str
        Path to the audio file (e.g., .wav)

    Returns
    -------
    dict
        Sentiment analysis result: {"sentiment": str, "confidence": float}
    """

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # Initialize OpenSMILE (using the 'emo_large' configuration for emotion features)
    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.emobase,
        feature_level=opensmile.FeatureLevel.Functionals,
    )

    # Extract acoustic features
    features = smile.process_file(audio_path)
    features = features.fillna(0)  # handle NaNs

    # Optionally scale features (for model compatibility)
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # --- Mocked or Pretrained Model ---
    # You can train your own model and save with joblib.dump(model, "sentiment_model.pkl")
    model_path = "sentiment_model.pkl"
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        # Temporary dummy model for demonstration
        X_dummy = np.random.rand(10, scaled_features.shape[1])
        y_dummy = np.random.choice(["positive", "negative", "neutral"], size=10)
        model = LogisticRegression(max_iter=200)
        model.fit(X_dummy, y_dummy)
        joblib.dump(model, model_path)

    # Predict sentiment
    probs = model.predict_proba(scaled_features)[0]
    label = model.classes_[np.argmax(probs)]
    confidence = float(np.max(probs))

    return label
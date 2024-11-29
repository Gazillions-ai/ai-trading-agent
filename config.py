"""Configuration settings for the AI Trading Agent."""

# Data Processing
BATCH_SIZE = 32  # Number of items to process in parallel
CACHE_SIZE = 1000  # Number of items to cache
MAX_TEXT_LENGTH = 512  # Maximum length of text to analyze

# Model Settings
MODEL_NAME = "ProsusAI/finbert"  # Sentiment analysis model
DEVICE = "cuda"  # Use "cuda" for GPU, "cpu" for CPU

# Trading Signal Parameters
SIGNAL_THRESHOLDS = {
    "STRONG_BUY": 0.8,
    "BUY": 0.5,
    "NEUTRAL": 0.0,
    "SELL": -0.5,
    "STRONG_SELL": -0.8
}

# Sentiment Analysis
SENTIMENT_THRESHOLDS = {
    "POSITIVE": 0.05,
    "NEGATIVE": -0.05
}

# Keywords for filtering
CRYPTO_KEYWORDS = [
    "crypto", "coin", "token", "meme", "$",
    "btc", "eth", "sol", "ada", "xrp"
]

# File Paths
DATA_DIRS = {
    "RAW": "data/raw",
    "PROCESSED": "data/processed",
    "ANALYSIS": "data/analysis",
    "SIGNALS": "data/signals"
}

# Dashboard Settings
DASHBOARD_CONFIG = {
    "UPDATE_INTERVAL": 60,  # seconds
    "MAX_TWEETS_DISPLAY": 100,
    "CHART_THEME": "plotly_dark"
}

# Error Handling
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

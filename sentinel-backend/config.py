import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Database
DB_NAME = "sentinel.db"

# Thresholds
CRS_CRITICAL_THRESHOLD = 0.85
CRS_HIGH_THRESHOLD = 0.60
CRS_MEDIUM_THRESHOLD = 0.35
CRS_LOW_THRESHOLD = 0.15

# Demo Config
DEMO_DURATION_SECONDS = 120

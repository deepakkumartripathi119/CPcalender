import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Calendar Configuration
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'primary'
# Local user's email or 'primary' if using the service account's own calendar
TARGET_CALENDAR_ID = os.environ.get('GOOGLE_CALENDAR_ID', 'primary')

# Google Cloud Service Account Key (JSON string)
# WE DO NOT DEFAULT THIS to avoid accidental usage of empty keys.
# It must be provided in the environment.
GCP_SA_KEY = os.environ.get('GCP_SA_KEY')

# CLIST API Configuration
CLIST_USERNAME = os.environ.get('CLIST_USERNAME')
CLIST_API_KEY = os.environ.get('CLIST_API_KEY')
CLIST_API_BASE_URL = "https://clist.by/api/v4"

def validate_config():
    """Checks if essential configuration is present."""
    missing = []
    if not GCP_SA_KEY:
        missing.append("GCP_SA_KEY")
    
    # We warn but don't fail immediately if CLIST is missing, 
    # as Codeforces might still work without it (using direct API).
    if not CLIST_USERNAME or not CLIST_API_KEY:
        print("WARNING: CLIST_USERNAME or CLIST_API_KEY not found. CLIST platforms will be skipped.")
    
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

import datetime
import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import config

def auth_service_account():
    """Authenticates using the Service Account Key from env vars."""
    if not config.GCP_SA_KEY:
        raise ValueError("GCP_SA_KEY not found in environment variables.")
        
    service_account_info = json.loads(config.GCP_SA_KEY)
    creds = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=config.SCOPES
    )
    return creds

def get_calendar_service():
    """Returns an authenticated Google Calendar service resource."""
    creds = auth_service_account()
    service = build('calendar', 'v3', credentials=creds)
    return service

def add_to_calendar(service, contest):
    """
    Adds a contest to the Google Calendar.
    
    Expected `contest` dictionary format:
    {
        "id": str,          # Unique ID for the event (without prefix, prefix is handled here if needed, or pre-prefixed)
                            # Actually, it's better if the caller handles uniqueness prefixes (e.g. 'cf123', 'lc456')
        "name": str,        # Event Summary
        "start_time": datetime, # datetime object (Timezone Aware - preferably UTC)
        "duration": int,    # Duration in seconds
        "url": str          # Link to the contest
    }
    """
    
    # We assume 'id' passed here is globally unique for the calendar (e.g. "cf1234", "lc5678")
    unique_id = contest['id']
    
    # Timezone Handling: Ensure event is localized to IST
    ist_zone = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    
    # Ensure start_time is aware
    if contest['start_time'].tzinfo is None:
        contest['start_time'] = contest['start_time'].replace(tzinfo=datetime.timezone.utc)
        
    start_ist = contest['start_time'].astimezone(ist_zone)
    end_ist = start_ist + datetime.timedelta(seconds=contest['duration'])
    
    # Format as ISO strings
    start_str = start_ist.isoformat()
    end_str = end_ist.isoformat()
    
    event_body = {
        'id': unique_id, 
        'summary': contest['name'], 
        'description': f"Link: {contest['url']}",
        'start': {
            'dateTime': start_str,
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_str,
            'timeZone': 'Asia/Kolkata',
        }, 
    }

    try:
        service.events().insert(calendarId=config.TARGET_CALENDAR_ID, body=event_body).execute()
        print(f"ADDED: {contest['name']}")
    except HttpError as error:
        if error.resp.status == 409:
            print(f"EXISTS: {contest['name']}")
        else:
            print(f"Error adding {contest['name']}: {error}")

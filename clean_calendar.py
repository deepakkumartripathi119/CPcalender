import config
from utils import google_calendar
import datetime

def clean_calendar():
    print("--- Starting Calendar Cleanup ---")
    try:
        config.validate_config()
    except Exception as e:
        print(f"Config Error: {e}")
        return

    service = google_calendar.get_calendar_service()
    
    # Prefixes used by the app to identify its events
    # cf: Codeforces, lc: LeetCode, cc: CodeChef, ac: AtCoder, testint: Integration Tests
    PREFIXES = ('cf', 'lc', 'cc', 'ac', 'testint')
    
    page_token = None
    total_deleted = 0
    
    print("Scanning calendar for bot events...")
    
    while True:
        events_result = service.events().list(
            calendarId=config.TARGET_CALENDAR_ID,
            # We don't set timeMin to ensure we clean up everything including past tests if any
            singleEvents=True,
            pageToken=page_token
        ).execute()
        
        events = events_result.get('items', [])

        for event in events:
            uid = event.get('id', '')
            summary = event.get('summary', 'No Title')
            
            if uid.startswith(PREFIXES):
                print(f"Deleting: [{uid}] {summary}")
                try:
                    service.events().delete(
                        calendarId=config.TARGET_CALENDAR_ID, 
                        eventId=uid
                    ).execute()
                    total_deleted += 1
                except Exception as e:
                    print(f"Failed to delete {uid}: {e}")
        
        page_token = events_result.get('nextPageToken')
        if not page_token:
            break
            
    print(f"\nCleanup complete. Deleted {total_deleted} events.")

if __name__ == "__main__":
    clean_calendar()

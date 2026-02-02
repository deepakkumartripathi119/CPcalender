import config
from utils import google_calendar
from platforms import codeforces, leetcode, codechef, atcoder

def main():
    # 1. Validate environment
    print("--- CP Calendar Sync Starting ---")
    try:
        config.validate_config()
        print(f"Target Calendar: {config.TARGET_CALENDAR_ID}")
        if config.TARGET_CALENDAR_ID == 'primary':
            print("WARNING: Using Service Account's primary calendar (default).") 
            print("Expected behavior? If not, check GOOGLE_CALENDAR_ID secret.")
            
    except EnvironmentError as e:
        print(f"Startup Error: {e}")
        print("Please ensure you have set the necessary environment variables.")
        # Proceeding might fail if critical keys are missing, but we let individual modules handle their failures too.
        # However, for GCP_SA_KEY, google_calendar will fail. 

    # 2. Authenticate Google Calendar
    try:
        service = google_calendar.get_calendar_service()
        
        # --- DEBUGGING IDENTITY ---
        creds = google_calendar.auth_service_account()
        sa_email = creds.service_account_email
        print(f"Authenticated as Service Account: {sa_email}")
        
        target = config.TARGET_CALENDAR_ID
        print(f"Target Calendar ID: {target[:3]}...{target[-10:] if len(target) > 10 else ''} (Length: {len(target)})")
        
        if target == 'primary' or target == sa_email:
            print("\n!!! CRITICAL WARNING !!!")
            print(f"You are saving events to the Service Account's OWN calendar ('{target}').")
            print("You will NOT see these on your personal Gmail unless you explicitly add/share the Service Account's calendar.")
            print("FIX: Set GOOGLE_CALENDAR_ID secret to your PERSONAL GMAIL address.")
            print("!!! ------------------ !!!\n")
            
    except ValueError as e:
        print(f"Google Calendar Auth Failed: {e}")
        return
    except Exception as e:
        print(f"Google Calendar Connection Failed: {e}")
        return

    # 3. Define platforms to fetch
    platforms = [
        ("Codeforces", codeforces),
        ("LeetCode", leetcode),
        ("CodeChef", codechef),
        ("AtCoder", atcoder),
    ]

    # 4. Fetch and Add
    total_added = 0
    for name, module in platforms:
        print(f"\n--- Fetching {name} ---")
        contests = module.get_contests()
        print(f"Found {len(contests)} upcoming contests.")
        
        for c in contests:
            try:
                google_calendar.add_to_calendar(service, c)
                total_added += 1
            except Exception as e:
                print(f"Failed to add {c['name']}: {e}")

    print(f"\nDone! Processed all platforms.")

if __name__ == '__main__':
    main()
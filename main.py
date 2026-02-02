import config
from utils import google_calendar
from platforms import codeforces, leetcode, codechef, atcoder

def main():
    # 1. Validate environment
    try:
        config.validate_config()
    except EnvironmentError as e:
        print(f"Startup Error: {e}")
        print("Please ensure you have set the necessary environment variables.")
        # Proceeding might fail if critical keys are missing, but we let individual modules handle their failures too.
        # However, for GCP_SA_KEY, google_calendar will fail. 

    # 2. Authenticate Google Calendar
    try:
        service = google_calendar.get_calendar_service()
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
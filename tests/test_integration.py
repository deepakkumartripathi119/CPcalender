import sys
import os
import unittest

# Add parent directory to path to allow importing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from platforms import codeforces, leetcode, codechef, atcoder

class TestContestFetching(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\n--- Starting Integration Tests ---")
        try:
            config.validate_config()
            print("Environment configuration verified.")
        except Exception as e:
            print(f"Configuration Warning: {e}")

    def test_codeforces(self):
        print("\nTesting Codeforces...")
        contests = codeforces.get_contests()
        print(f"Fetched {len(contests)} contests.")
        self.assertIsInstance(contests, list)
        if contests:
            self.assertTrue('id' in contests[0])
            self.assertTrue('name' in contests[0])

    def test_leetcode(self):
        print("\nTesting LeetCode (via CLIST)...")
        contests = leetcode.get_contests()
        print(f"Fetched {len(contests)} contests.")
        self.assertIsInstance(contests, list)

    def test_codechef(self):
        print("\nTesting CodeChef (via CLIST)...")
        contests = codechef.get_contests()
        print(f"Fetched {len(contests)} contests.")
        self.assertIsInstance(contests, list)

    def test_atcoder(self):
        print("\nTesting AtCoder (via CLIST)...")
        contests = atcoder.get_contests()
        print(f"Fetched {len(contests)} contests.")
        self.assertIsInstance(contests, list)

    def test_z_google_calendar_auth(self):
        """
        Verifies that we can authenticate with Google Calendar API.
        Uses a read-only call (list calendars) to check credentials.
        """
        print("\nTesting Google Calendar Authentication...")
        try:
            from utils import google_calendar
            service = google_calendar.get_calendar_service()
            # Try a lightweight read operation
            calendar_list = service.calendarList().list(maxResults=1).execute()
            print("Successfully authenticated and fetched calendar list.")
            self.assertTrue('items' in calendar_list)
        except Exception as e:
            self.fail(f"Google Calendar Auth Failed: {e}")

    def test_zz_real_calendar_flow(self):
        """
        Verifies REAL insertion and deletion in Google Calendar.
        Creates an event, confirms it exists, and then deletes it.
        """
        print("\nTesting Real Calendar Insertion & Deletion...")
        from utils import google_calendar
        import datetime
        import time
        
        service = None
        # Google Calendar IDs must be lowercase a-v and 0-9.
        test_id = f"testint{int(time.time())}"
        
        try:
            service = google_calendar.get_calendar_service()
            
            # Sample contest data
            sample_contest = {
                "id": test_id,
                "name": "ANTIGRAVITY_INTEGRATION_TEST_EVENT",
                "start_time": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10),
                "duration": 600, # 10 mins
                "url": "https://example.com"
            }

            # 1. Insert
            print(f"Inserting test event {test_id}...")
            google_calendar.add_to_calendar(service, sample_contest)
            
            # 2. Verify existence
            print("Verifying event in calendar...")
            try:
                event = service.events().get(calendarId=config.TARGET_CALENDAR_ID, eventId=test_id).execute()
                self.assertEqual(event['summary'], "ANTIGRAVITY_INTEGRATION_TEST_EVENT")
                print("Event confirmed via API.")
            except Exception as e:
                self.fail(f"Verification failed (Event not found?): {e}")

        except Exception as e:
            self.fail(f"Test failed during insertion/verification: {e}")
        
        finally:
            # 3. Clean up (Always try to delete)
            if service:
                print(f"Cleaning up: Deleting event {test_id}...")
                try:
                    service.events().delete(calendarId=config.TARGET_CALENDAR_ID, eventId=test_id).execute()
                    print("Event deleted successfully.")
                except Exception as e:
                    print(f"WARNING: Failed to delete test event {test_id}. Please remove manually. Error: {e}")

if __name__ == '__main__':
    unittest.main()

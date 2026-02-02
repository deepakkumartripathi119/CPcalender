from utils import clist_api
import datetime

def get_contests():
    """
    Fetches upcoming LeetCode contests via CLIST.
    """
    raw_contests = clist_api.fetch_clist_resources('leetcode.com')
    standardized_contests = []
    
    for c in raw_contests:
        try:
            # Parse time. CLIST returns UTC strings like "2025-11-28T20:00:00"
            # We assume it is UTC.
            start_str = c['start']
            if not start_str.endswith('Z') and '+' not in start_str:
                start_dt = datetime.datetime.fromisoformat(start_str).replace(tzinfo=datetime.timezone.utc)
            else:
                 # Minimal handling for Z or offsets if they appear
                start_dt = datetime.datetime.fromisoformat(start_str.replace('Z', '+00:00'))

            contest = {
                "id": f"lc{c['id']}", # Prefix to avoid collision
                "name": f"LC: {c['event']}",
                "start_time": start_dt,
                "duration": c['duration'],
                "url": c['href']
            }
            standardized_contests.append(contest)
        except ValueError as e:
            print(f"Error parsing date for {c.get('event')}: {e}")
            continue

    return standardized_contests

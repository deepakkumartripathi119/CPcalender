from utils import clist_api
import datetime

def get_contests():
    """
    Fetches upcoming CodeChef contests via CLIST.
    """
    raw_contests = clist_api.fetch_clist_resources('codechef.com')
    standardized_contests = []
    
    for c in raw_contests:
        try:
            start_str = c['start']
            # Assume UTC
            if not start_str.endswith('Z') and '+' not in start_str:
                start_dt = datetime.datetime.fromisoformat(start_str).replace(tzinfo=datetime.timezone.utc)
            else:
                start_dt = datetime.datetime.fromisoformat(start_str.replace('Z', '+00:00'))

            contest = {
                "id": f"cc{c['id']}", 
                "name": f"CC: {c['event']}",
                "start_time": start_dt,
                "duration": c['duration'],
                "url": c['href']
            }
            standardized_contests.append(contest)
        except ValueError as e:
            print(f"Error parsing date for {c.get('event')}: {e}")
            continue

    return standardized_contests

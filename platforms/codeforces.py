import requests
import datetime

def get_contests():
    """
    Fetches upcoming Codeforces contests using the official Codeforces API.
    Returns standardized contest objects.
    """
    try:
        url = "https://codeforces.com/api/contest.list"
        resp = requests.get(url, params={"gym": "false"}).json()
        
        if resp["status"] != "OK":
            print("Codeforces API returned non-OK status")
            return []
            
        # Filter for upcoming contests (Phase must be 'BEFORE')
        upcoming_raw = [c for c in resp["result"] if c["phase"] == "BEFORE"]
        
        standardized_contests = []
        for c in upcoming_raw:
            # Codeforces 'startTimeSeconds' is a unix timestamp
            start_dt = datetime.datetime.fromtimestamp(c['startTimeSeconds'], datetime.timezone.utc)
            
            contest = {
                "id": f"cf{c['id']}v4", # Preserving ID format from previous main.py for dedupe
                "name": f"CF: {c['name']}",
                "start_time": start_dt,
                "duration": c['durationSeconds'],
                "url": f"https://codeforces.com/contest/{c['id']}"
            }
            standardized_contests.append(contest)
            
        return standardized_contests

    except Exception as e:
        print(f"Error fetching Codeforces: {e}")
        return []

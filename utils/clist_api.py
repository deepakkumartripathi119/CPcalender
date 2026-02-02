import requests
import datetime
import config

def get_resource_id(resource_name, headers):
    """
    Resolves a resource name (e.g., 'leetcode.com') to its CLIST ID.
    """
    url = f"{config.CLIST_API_BASE_URL}/resource/"
    params = {'name': resource_name}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        objects = data.get('objects', [])
        if objects:
            return objects[0]['id']
        else:
            print(f"Resource not found: {resource_name}")
            return None
    except Exception as e:
        print(f"Error resolving resource {resource_name}: {e}")
        return None

def fetch_clist_resources(resource_name, limit=20):
    """
    Fetches upcoming contests for a specific resource (platform) from CLIST.
    
    Args:
        resource_name (str): e.g., 'leetcode.com', 'codechef.com', 'atcoder.jp'
        limit (int): Max number of contests to fetch. Defaults to 20.
        
    Returns:
        list: A list of contest dictionaries from CLIST.
    """
    if not config.CLIST_USERNAME or not config.CLIST_API_KEY:
        print(f"Skipping {resource_name}: CLIST credentials not set.")
        return []

    headers = {
        'Authorization': f"ApiKey {config.CLIST_USERNAME}:{config.CLIST_API_KEY}"
    }

    # 1. Get Resource ID
    resource_id = get_resource_id(resource_name, headers)
    if not resource_id:
        return []

    # 2. Fetch Contests
    endpoint = f"{config.CLIST_API_BASE_URL}/contest/"
    
    # Calculate start time (now)
    now = datetime.datetime.now(datetime.timezone.utc)
    now_str = now.strftime('%Y-%m-%dT%H:%M:%S')

    params = {
        'resource_id': resource_id,
        'start__gte': now_str, # Only upcoming
        'order_by': 'start',
        'limit': limit,
    }
    
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('objects', [])
    except requests.RequestException as e:
        print(f"Error fetching from CLIST ({resource_name}): {e}")
        try:
             print(f"Response Content: {e.response.text}")
        except:
             pass
        return []

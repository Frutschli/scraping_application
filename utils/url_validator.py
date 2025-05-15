import requests

def validate_url(url):
    """
    Validates if a URL is reachable.
    
    Args:
        url (str): The URL to validate
        
    Returns:
        bool: True if the URL is valid and reachable, False otherwise
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            print(f"[ERROR] Unable to reach URL: {url} (Status code: {response.status_code})")
            return False
    except requests.RequestException as e:
        print(f"[ERROR] Invalid URL or connection issue: {e}")
        return False
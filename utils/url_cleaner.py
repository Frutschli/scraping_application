"""
Module for cleaning and normalizing URLs before processing.
"""
import re
import urllib.parse

def clean_url(url):
    """
    Clean and normalize a URL by:
    - Adding https:// if no protocol is specified
    - Removing trailing slashes
    - Preserving www in domain names
    - Removing tracking parameters (utm_*, fbclid, etc.)
    - Decoding URL-encoded characters
    
    Args:
        url (str): The URL to clean
        
    Returns:
        str: The cleaned URL
    """
    if not url:
        return url
        
    # Trim whitespace
    url = url.strip()
    
    # Add protocol if missing
    if not re.match(r'^https?://', url):
        url = 'https://' + url
    
    # Parse the URL
    parsed_url = urllib.parse.urlparse(url)
    
    # Keep the domain as is, including www if present
    netloc = parsed_url.netloc
    
    # Clean the path
    path = parsed_url.path
    if path.endswith('/'):
        path = path[:-1]  # Remove trailing slash
    
    # Clean query parameters - focus on removing tracking params (utm_*, fbclid, etc.)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    tracking_param_prefixes = ('utm_', 'fbclid', 'gclid', '_ga', 'ref', 'source')
    cleaned_params = {
        k: v for k, v in query_params.items() 
        if not any(k.startswith(prefix) for prefix in tracking_param_prefixes)
    }
    
    # Rebuild query string
    query_string = urllib.parse.urlencode(cleaned_params, doseq=True)
    
    # Rebuild the URL with cleaned components
    cleaned_url = urllib.parse.urlunparse((
        parsed_url.scheme,
        netloc,
        path,
        parsed_url.params,
        query_string,
        parsed_url.fragment
    ))
    
    return cleaned_url

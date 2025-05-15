from ollama import chat
import os
import sys
import re
import requests
import subprocess
import yaml

class Config:
    def __init__(self, config_file='config.yaml'):
        with open(config_file, 'r') as file:
            config_data = yaml.safe_load(file)
            for key, value in config_data.items():
                setattr(self, key, value)
config = Config()

# Add the Scrapy project to the Python path
scrapy_project_path = r".\quelltext_scraper"

# user interdace module



final_response = ""

def validate_url(url):
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

def process_website():
    global final_response  # Use the global variable
    
    print("Thinking...")
    # Read the HTML file content
    with open('quelltext.txt', 'r', encoding='utf-8') as file:
        website = file.read()
    
    complete_response = ""
    stream = chat(
        model='llama3.2:3b',
        messages=[
            {'role': 'system', 'content': "You are a computer Program trying to figure out who the Geschäftsführer of a website is. ONLY ANSWER IN THIS FORMAT: 'information_type: information' (example). Provide ONLY this: impressum_url, name_of_Geschäftsführer, relevant_emails, phone_numbers"},
            {'role': 'user', 'content': "Here are some links and text we could crawl from the website." + website},
        ],
        stream=True,
    )
    
    for chunk in stream:
        chunk_content = chunk['message']['content']
        complete_response += chunk_content  # Accumulate the chunks
        print(chunk_content, end='', flush=True)  # Still print as before
    
    print()
    match = re.search(r'impressum_url:\s*(.*?)(?:\n|$)', complete_response)
    if match:
        impressum_url = match.group(1).strip()
        if impressum_url == current_url:
            final_response = complete_response  # Save the complete response
            return True, None, complete_response
        else:
            print(f"URL doesn't match. Found: {impressum_url}")
            # If the URL found is valid, we'll use it for the next iteration
            if impressum_url.startswith(("http://", "https://")):
                return False, impressum_url, None
    else:
        print("No impressum_url found in the response")
    
    return False, None, None

def run_single_iteration(url):
    # Create a temporary script file
    with open('temp_spider_run.py', 'w') as f:
        f.write(f'''
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import sys

# Add the Scrapy project to the Python path
sys.path.append(r"{scrapy_project_path}")
from quelltext_scraper.spiders.quelltext_spider import QuelltextSpider

os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'quelltext_scraper.settings')
process = CrawlerProcess(get_project_settings())
   
# Set the provided URL
QuelltextSpider.provided_urls = ["{url}"]
   
process.crawl(QuelltextSpider)
process.start()
        ''')
    
    # Run the temporary script as a subprocess
    subprocess.run([sys.executable, 'temp_spider_run.py'], check=True)
    
    # After spider completes, process the website
    return process_website()

if __name__ == "__main__":
    # Prompt the user for a URL
    user_url = input("Please enter a URL (example: " + config.standard_url + "):" ).strip()
   
    # Use a default URL if the user presses enter without typing anythingclear
    if not user_url:
        user_url = config.standard_url
        print(f"[INFO] No URL provided. Using example URL: {config.standard_url}")
    
    # Flag to control the loop
    continue_processing = True
    current_url = user_url
    iteration = 0
    
    while continue_processing and iteration < config.max_iterations:
        iteration += 1
        print(f"\n[INFO] Iteration {iteration} with URL: {current_url}")
        
        # Validate the provided URL
        if validate_url(current_url):
            # Run spider and process website
            try:
                success, new_url, response_text = run_single_iteration(current_url)
                
                if success:
                    # If we found the matching impressum_url, we're done
                    print(f"[SUCCESS] Found matching impressum_url: {current_url}")
                    print()
                    print("Final Information:")
                    print(response_text)  # Print the complete response
                    continue_processing = False
                elif new_url:
                    # If a new URL was returned, use it for the next iteration
                    print(f"[INFO] Continuing with new URL: {new_url}")
                    current_url = new_url
                else:
                    # If no valid URL was found, stop
                    print("[INFO] No valid impressum_url found. Stopping...")
                    continue_processing = False
            except Exception as e:
                print(f"[ERROR] An error occurred: {e}")
                continue_processing = False
        else:
            print(f"[ERROR] The URL {current_url} is not reachable. Exiting...")
            continue_processing = False
    
    if iteration >= config.max_iterations:
        print(f"[WARNING] Reached maximum iterations ({config.max_iterations}). Stopping to prevent infinite loop.")
    
    print("[INFO] Process complete.")
    
    # Clean up the temporary file
    if os.path.exists('temp_spider_run.py'):
        os.remove('temp_spider_run.py')
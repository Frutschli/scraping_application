#!/usr/bin/env python3
"""
Main module that orchestrates the website crawling and information extraction process.
"""
import sys
from config import Config
from utils.url_validator import validate_url
from utils.url_cleaner import clean_url  # Import the new URL cleaner
from quelltext_scraper.spider_manager import SpiderManager
from data_extractor.html_parser import HTMLParser
from llm_processor.ollama_client import OllamaClient
from ui.console_interface import ConsoleInterface

def main():
    """
    Main function that orchestrates the application flow.
    """
    # Initialize configuration
    config = Config()
    
    # Initialize modules
    ui = ConsoleInterface(config)
    spider_manager = SpiderManager(config)
    html_parser = HTMLParser(config)
    ollama_client = OllamaClient(config)
    
    # Get initial URL from user
    url_input = ui.get_initial_url()
    
    # Clean the URL before processing
    current_url = clean_url(url_input)
    if current_url != url_input:
        ui.display_url_cleaned(url_input, current_url)
    
    # Process control variables
    continue_processing = True
    iteration = 0
    process_type = config.standard_process 
    
    # Main processing loop
    while continue_processing != False and iteration < config.max_iterations:
        iteration += 1
        ui.display_iteration_start(iteration, current_url)
        
        # Validate the provided URL
        if validate_url(current_url):
            try:
                # Run spider
                if spider_manager.run_spider(current_url, process_type):
                    # Load crawled data
                    website_content = html_parser.load_crawled_data(process_type)
                    if process_type == "process_text":
                        continue_processing = False
                    
                    # Process website with LLM
                    if process_type == "process_links":
                        success, new_url, response_text = ollama_client.process_website_data(
                            website_content, current_url
                        )
                    elif process_type == "process_text":
                        success, new_url, response_text = ollama_client.process_website_text(
                            website_content, current_url
                        )


                    if success:
                        # We found what we were looking for
                        ui.display_success(current_url, response_text, process_type)
                        #conimue_processing = False  
                        process_type = "process_text"                    
                    elif new_url:
                        # Clean the new URL before continuing 
                        cleaned_new_url = clean_url(new_url)
                        if cleaned_new_url != new_url:
                            ui.display_url_cleaned(new_url, cleaned_new_url)
                            new_url = cleaned_new_url
                            
                        # Continue with a new URL
                        ui.display_continue_with_new_url(new_url)
                        current_url = new_url
                    else:
                        # No valid URL found
                        ui.display_no_valid_url()
                        continue_processing = False
                else:
                    ui.display_error("Spider failed to run properly.")
                    continue_processing = False
            except Exception as e:
                ui.display_error(f"An error occurred: {e}")
                continue_processing = False
        else:
            ui.display_error(f"The URL {current_url} is not reachable. Exiting...")
            continue_processing = False
    
    # Check if we reached the maximum number of iterations
    if iteration >= config.max_iterations:
        ui.display_max_iterations_warning()
    
    ui.display_completion()

if __name__ == "__main__":
    main()

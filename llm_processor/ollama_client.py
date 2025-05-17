from ollama import chat
from pydantic import BaseModel
import re

class OllamaClient:
    """
    Handles interactions with the Ollama LLM API.
    """
    
    def __init__(self, config):
        """
        Initialize the OllamaClient.
        
        Args:
            config (Config): Configuration object containing model settings
        """
        self.config = config
        
    def process_website_data(self, website_content, current_url):
        """
        Processes website data through the LLM to extract specific information.
        
        Args:
            website_content (str): The website content to process
            current_url (str): The current URL being processed
            
        Returns:
            tuple: (success, new_url, response_text)
                - success (bool): Whether the processing was successful
                - new_url (str): A new URL to process if found
                - response_text (str): The response from the LLM
        """
        print("Thinking...")
        complete_response = ""
        stream = chat(
            model=self.config.llm_model,
            messages=[
                {'role': 'system', 'content': "You are a computer Program trying to figure out who the Geschäftsführer or Geschäftsleitung or similar of a website is. ONLY ANSWER IN THIS FORMAT: 'impressum_url: impressum' (example). Provide ONLY this: impressum_url, name_of_Geschäftsführer, relevant_emails, phone_numbers"},
                {'role': 'user', 'content': "Here are some links and text we could crawl from the website." + website_content},
            ],
            stream=True,
            options={'temperature': 0}
        )

        for chunk in stream:
            chunk_content = chunk['message']['content']
            complete_response += chunk_content  # Accumulate the chunks
            print(chunk_content, end='', flush=True)  # Still print as before
        
        print()
        
        # Process the response to find impressum URL
        match = re.search(r'impressum_url:\s*(.*?)(?:\n|$)', complete_response)
        if match:
            impressum_url = match.group(1).strip()
            if impressum_url == current_url:
                return True, None, complete_response
            else:
                print(f"URL doesn't match. Found: {impressum_url}")
                # If the URL found is valid, we'll use it for the next iteration
                if impressum_url.startswith(("http://", "https://")):
                    return False, impressum_url, None
        else:
            print("No impressum_url found in the response")
        
        return False, None, None
    
    def process_website_text(self, website_content, current_url):
        """
        Processes website text through the LLM to extract specific information.
        
        Args:
            website_content (str): The website content to process
            current_url (str): The current URL being processed
            
        Returns:
            tuple: (success, new_url, response_text)
                - success (bool): Whether the processing was successful
                - new_url (str): A new URL to process if found
                - response_text (str): The response from the LLM
        """
        print("Thinking...")
        
        complete_response = ""
        class Text(BaseModel):
            name_of_Geschäftsführer: list[str] | None
            relevant_emails: list[str] | None
            relevant_phone_numbers: list[str] | None
        response = chat(
            model=self.config.llm_model,
            messages=[
                {'role': 'system', 'content': "You are a computer Program trying to extract data from this website. ONLY DATA THAT IS ACTUALLY PRESENT"},
                {'role': 'user', 'content': "Here are some links and text we could crawl from the website." + website_content},
            ],   
            format=Text.model_json_schema(),
            options={'temperature': 0}
            )
        text_data = Text.model_validate_json(response.message.content)
        complete_response = str(text_data)
        print()
        
        
        return True, None, complete_response
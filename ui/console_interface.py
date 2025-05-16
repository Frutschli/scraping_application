class ConsoleInterface:
    """
    Handles user interaction through the console.
    """
    
    def __init__(self, config):
        """
        Initialize the ConsoleInterface.
        
        Args:
            config (Config): Configuration object
        """
        self.config = config
        
    def get_initial_url(self):
        """
        Prompts the user for a URL and returns it.
        
        Returns:
            str: The URL provided by the user or the default URL
        """
        user_url = input(f"Please enter a URL (example: {self.config.standard_url}): ").strip()
        
        # Use a default URL if the user presses enter without typing anything
        if not user_url:
            user_url = self.config.standard_url
            print(f"[INFO] No URL provided. Using example URL: {self.config.standard_url}")
        
        return user_url
    
    def display_url_cleaned(self, original_url, cleaned_url):
        """
        Displays information about URL cleaning.
        
        Args:
            original_url (str): The original URL provided
            cleaned_url (str): The cleaned URL
        """
        print(f"[INFO] URL cleaned: '{original_url}' → '{cleaned_url}'")
    
    def display_iteration_start(self, iteration, url):
        """
        Displays information about the current iteration.
        
        Args:
            iteration (int): The current iteration number
            url (str): The URL being processed
        """
        print(f"\n[INFO] Iteration {iteration} with URL: {url}")
    
    def display_success(self, url, response_text):
        """
        Displays success message and the final information.
        
        Args:
            url (str): The URL that was successfully processed
            response_text (str): The response text to display
        """
        print(f"[SUCCESS] Found matching impressum_url: {url}")
        print()
        print("Final Information:")
        print(response_text)
    
    def display_continue_with_new_url(self, new_url):
        """
        Displays message about continuing with a new URL.
        
        Args:
            new_url (str): The new URL to continue with
        """
        print(f"[INFO] Continuing with new URL: {new_url}")
    
    def display_no_valid_url(self):
        """
        Displays message about no valid URL being found.
        """
        print("[INFO] No valid impressum_url found. Stopping...")
    
    def display_error(self, message):
        """
        Displays an error message.
        
        Args:
            message (str): The error message to display
        """
        print(f"[ERROR] {message}")
    
    def display_max_iterations_warning(self):
        """
        Displays warning about reaching maximum iterations.
        """
        print(f"[WARNING] Reached maximum iterations ({self.config.max_iterations}). Stopping to prevent infinite loop.")
    
    def display_completion(self):
        """
        Displays message about process completion.
        """
        print("[INFO] Process complete.")

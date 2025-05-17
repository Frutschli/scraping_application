class HTMLParser:
    """
    Handles the extraction and processing of HTML content from crawled data.
    """
    
    def __init__(self, config):
        """
        Initialize the HTMLParser.
        
        Args:
            config (Config): Configuration object containing paths and settings
        """
        self.config = config
        
    def load_crawled_data(self, process_type):
        """
        Loads data from the crawler output file.
        
        Returns:
            str: The content of the crawled data
        """
        if process_type == "process_links":
          
            try:
                with open(self.config.output_file, 'r', encoding='utf-8') as file:
                    return file.read()
            except FileNotFoundError:
                print(f"[ERROR] Crawled data file not found: {self.config.output_file}")
                return ""
        elif process_type == "process_text":
            try:
                with open(self.config.text_output_file, 'r', encoding='utf-8') as file:
                    return file.read()
            except FileNotFoundError:
                print(f"[ERROR] Crawled data file not found: {self.config.text_output_file}")
                return ""
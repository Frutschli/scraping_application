import yaml

class Config:
    def __init__(self, config_file='config/config.yaml'):
        try:
            with open(config_file, 'r') as file:
                config_data = yaml.safe_load(file)
                for key, value in config_data.items():
                    setattr(self, key, value)
        except FileNotFoundError:
            print(f"[ERROR] Configuration file {config_file} not found.")
            # Set some defaults
            self.standard_url = "https://www.2txt.de/"
            self.max_iterations = 5
            self.scrapy_project_path = r".\quelltext_scraper"
            self.output_file = "quelltext.txt"
            self.llm_model = "llama3.2:3b"
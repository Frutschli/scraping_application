import os
import sys
import subprocess

class SpiderManager:
    """
    Manages Scrapy spiders for web crawling.
    """
    
    def __init__(self, config):
        """
        Initialize the SpiderManager.
        
        Args:
            config (Config): Configuration object containing paths and settings
        """
        self.config = config
        
    def run_spider(self, url):
        """
        Runs the Scrapy spider for a given URL.
        
        Args:
            url (str): The URL to crawl
            
        Returns:
            bool: True if the spider ran successfully, False otherwise
        """
        # Create a temporary script file
        with open(self.config.spider_temp_file, 'w') as f:
            f.write(f'''
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import sys

# Add the Scrapy project to the Python path
sys.path.append(r"{self.config.scrapy_project_path}")
from quelltext_scraper.spiders.quelltext_spider import QuelltextSpider

os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'quelltext_scraper.settings')
process = CrawlerProcess(get_project_settings())
   
# Set the provided URL
QuelltextSpider.provided_urls = ["{url}"]
   
process.crawl(QuelltextSpider)
process.start()
            ''')
        
        try:
            # Run the temporary script as a subprocess
            subprocess.run([sys.executable, self.config.spider_temp_file], check=True)
            return True
        except subprocess.SubprocessError as e:
            print(f"[ERROR] Spider execution failed: {e}")
            return False
        finally:
            # Clean up the temporary file
            if os.path.exists(self.config.spider_temp_file):
                os.remove(self.config.spider_temp_file)
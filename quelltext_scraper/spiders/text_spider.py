import scrapy
import re
from bs4 import BeautifulSoup

class TextSpider(scrapy.Spider):
    name = 'text'
    provided_urls = ["https://www.2txt.de/impressum"]
    
    def start_requests(self):
        for url in self.provided_urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        self.logger.info(f"Processing: {response.url}")
        
        # Initialize content collector and seen content tracker
        content_sections = []
        seen_texts = set()
        
        # Use Beautiful Soup for more flexibility with parsing
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Extract from common content containers
        content_elements = []
        
        # Main content containers
        content_containers = soup.select('article, section, .content, #content, main, [role="main"]')
        if content_containers:
            for container in content_containers:
                content_elements.append(("MAIN CONTENT", container))
        
        # If no main containers found, try with more generic containers
        if not content_containers:
            for tag in ['div', 'article', 'section']:
                for element in soup.find_all(tag):
                    if self._is_likely_content_element(element):
                        content_elements.append(("CONTENT SECTION", element))
        
        # 2. Also look specifically for contact information and impressum data
        contact_sections = soup.select('.contact, #contact, .impressum, #impressum, .imprint, #imprint')
        for section in contact_sections:
            content_elements.append(("CONTACT/IMPRESSUM", section))
        
        # 3. Process the collected elements
        for section_type, element in content_elements:
            text_content = self._extract_formatted_text(element)
            clean_text = text_content.strip()
            
            if clean_text and clean_text not in seen_texts:
                seen_texts.add(clean_text)
                content_sections.append(f"--- {section_type} ---\n{clean_text}\n")
        
        # 4. Final check for general paragraphs if we still have little content
        if not content_sections:
            paragraphs = []
            for p in soup.find_all('p'):
                clean_text = p.get_text(strip=True)
                if clean_text and len(clean_text) > 20 and clean_text not in seen_texts:
                    seen_texts.add(clean_text)
                    paragraphs.append(clean_text)
            
            if paragraphs:
                content_sections.append("--- PARAGRAPHS ---\n" + "\n\n".join(paragraphs))
        
        # Save the extracted content to a file
        filename = "website_text.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(content_sections))
        
        self.logger.info(f"Saved text content to {filename}")
    
    def _is_likely_content_element(self, element):
        if len(element.get_text(strip=True)) < 20:
            return False
        skip_patterns = ['nav', 'menu', 'footer', 'header', 'sidebar', 'widget', 'banner', 'cookie', 'popup', 'modal', 'cart', 'search', 'social']
        element_id = element.get('id', '').lower()
        element_class = ' '.join(element.get('class', [])).lower()
        for pattern in skip_patterns:
            if (pattern in element_id or pattern in element_class):
                return False
        text_length = len(element.get_text(strip=True))
        html_length = len(str(element))
        return html_length > 0 and text_length / html_length >= 0.2
    
    def _extract_formatted_text(self, element):
        result = []
        for header in element.select('h1, h2, h3, h4, h5'):
            text = header.get_text(strip=True)
            if text:
                level = int(header.name[1])
                prefix = '#' * level + ' '
                result.append(f"\n{prefix}{text}\n")
        for p in element.find_all(['p', 'li']):
            text = p.get_text(strip=True)
            if text:
                tag_type = '- ' if p.name == 'li' else ''
                result.append(f"{tag_type}{text}")
        for dt in element.find_all('dt'):
            term = dt.get_text(strip=True)
            dd = dt.find_next('dd')
            if term and dd:
                definition = dd.get_text(strip=True)
                result.append(f"{term}: {definition}")
        for table in element.find_all('table'):
            result.append("\nTABLE:")
            for row in table.find_all('tr'):
                cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                if cells:
                    result.append(" | ".join(cells))
            result.append("")
        return "\n\n".join(result)

import scrapy
from scrapy.utils.reactor import install_reactor

# Install the AsyncioSelectorReactor
install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")


class QuelltextSpider(scrapy.Spider):
    name = 'quelltext'
    provided_urls = ["https://www.2txt.de/"]
    seen_urls = set()

    async def start(self):
        for url in self.provided_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        extracted_content = []

        # Extract and format all <a> elements with full URLs
        for link in response.css('a'):
            text = link.css('::text').get()
            href = link.css('::attr(href)').get()
            if text and href:
                full_url = response.urljoin(href.strip())
                # Check for duplicate URLs
                if full_url not in self.seen_urls:
                    self.seen_urls.add(full_url)
                    extracted_content.append(f"Link: {full_url} ({text.strip()})")

        # Extract and format all <p> elements, including loose text between <br> tags
        paragraphs = response.xpath('//p//text() | //br/following-sibling::text()[1]').getall()
        combined_text = []

        # Clean up the extracted text
        for text in paragraphs:
            cleaned_text = text.strip()
            if cleaned_text:  # Only add non-empty lines
                combined_text.append(cleaned_text)

        if combined_text:
            extracted_content.append("Paragraph: " + " ".join(combined_text))

        # Save the extracted content to a file
        filename = "quelltext.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(extracted_content))

        self.logger.info("Crawling Complete")
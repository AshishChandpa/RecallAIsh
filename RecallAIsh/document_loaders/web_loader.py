import requests
from bs4 import BeautifulSoup

from .base_loader import BaseDocumentLoader


class WebDocumentLoader(BaseDocumentLoader):
    def __init__(self, scraper_type: str = "BeautifulSoup"):
        """
        Initialize the web document loader with a specific scraper type.

        :param scraper_type: The scraping method used (default: "BeautifulSoup").
        """
        self.scraper_type = scraper_type  # Only available in WebDocumentLoader

    def load(self, url: str) -> dict:
        """
        Load a web page document from a given URL and return a dictionary with keys
        like 'title', 'text_content', and any additional metadata.

        :param url: The URL of the web page to load.
        :return: A dictionary with the following keys:

            - title: The title of the web page.
            - text_content: The main text content of the web page.
            - metadata: A dictionary containing the following keys:

                - url: The URL of the web page.
                - file_type: The type of the document, always "web".
        """
        if self.scraper_type == "BeautifulSoup":
            return self._load_with_beautifulsoup(url)

        elif self.scraper_type == "Playwright":
            return self._load_with_playwright(url)

        elif self.scraper_type == "Selenium":
            return self._load_with_selenium(url)
        else:
            raise ValueError(f"Unsupported scraper type: {self.scraper_type}")

    def _load_with_playwright(self, url: str) -> dict:
        # Placeholder for Playwright implementation
        from ..web_scraper.playwright_scraper import PlaywrightScraper

        scrapper = PlaywrightScraper()
        return scrapper.extract_data(url)

    def _load_with_selenium(self, url: str) -> dict:
        # Placeholder for Selenium implementation
        from ..web_scraper.selenium_scraper import SeleniumScraper

        scrapper = SeleniumScraper()
        return scrapper.extract_data(url)

    def _load_with_beautifulsoup(self, url: str) -> dict:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "Untitled"
        text = soup.get_text(separator="\n")
        return {
            "title": title,
            "text_content": text,
            "metadata": {"url": url, "file_type": "web"},
        }

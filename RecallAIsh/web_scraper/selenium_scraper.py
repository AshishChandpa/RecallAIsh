from typing import Any, Dict, List
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from .base import BaseScraper, logger


class SeleniumScraper(BaseScraper):
    def __init__(self):
        self.driver = self._init_driver()

    def _init_driver(self):
        # if not self.driver:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")

        # Use webdriver_manager to handle driver installation
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        return self.driver

    def extract_data(self, url: str) -> Dict[str, Any]:
        try:
            # self._init_driver()
            self.driver.get(url)
            # wait = WebDriverWait(self.driver, 20)  # Increased wait for slow loading pages
            links = self.driver.find_elements(By.TAG_NAME, "a")
            urls = []
            for link in links:
                urls.append(link.get_attribute("href"))

            data = {
                "title": self.driver.title or "",
                "headings": [
                    h.text
                    for h in self.driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3")
                    if h.text
                ],
                "text_content": self.driver.find_element(By.TAG_NAME, "body").text
                or "",
                "images": [
                    img.get_attribute("src")
                    for img in self.driver.find_elements(By.TAG_NAME, "img")
                    if img.get_attribute("src")
                ],
                "urls": urls,
            }
            # self.driver.close()
            return data

        except Exception as e:
            logger.error(f"Selenium scraping failed: {str(e)}")
            raise

    def get_internal_links(self, url: str) -> List[dict]:
        try:
            self._init_driver()
            # self.driver.get(url)

            base_url = "/".join(url.split("/")[:3])
            links = self.driver.find_elements(By.TAG_NAME, "a")
            all_links = []

            for link in links:
                href = self.safe_get_attribute(link, "href")

                if href:
                    full_url = urljoin(base_url, href)
                    print(full_url)
                    link_data = self.extract_data(full_url)

                    if full_url.startswith(base_url):
                        all_links.append({"url": full_url, "link_data": link_data})

            return all_links

        except Exception as e:
            logger.error(f"Selenium link extraction failed: {str(e)}")
            raise

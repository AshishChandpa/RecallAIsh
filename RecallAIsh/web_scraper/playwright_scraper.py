import time
from typing import Any, Dict, List
from urllib.parse import urljoin

import playwright.sync_api as playwright

from .base import BaseScraper, logger


class PlaywrightScraper(BaseScraper):
    def __init__(self):
        self.browser = None

    def _init_browser(self):
        if not self.browser:
            playwright_instance = playwright.sync_playwright().start()
            self.browser = playwright_instance.chromium.launch(
                headless=True,
                args=["--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"],
            )

    def extract_data(self, url: str) -> Dict[str, Any]:
        try:
            self._init_browser()
            context = self.browser.new_context(ignore_https_errors=True)
            page = context.new_page()
            page.goto(
                url, wait_until="networkidle", timeout=60000
            )  # Increased timeout for slow loading pages

            data = {
                "title": page.title() or "",
                "headings": [
                    h.inner_text()
                    for h in page.query_selector_all("h1, h2, h3")
                    if h.inner_text()
                ],
                "text_content": page.inner_text("body") or "",
                "images": [
                    img.get_attribute("src")
                    for img in page.query_selector_all("img")
                    if img.get_attribute("src")
                ],
            }

            page.close()
            context.close()
            return data

        except Exception as e:
            logger.error(f"Playwright scraping failed: {str(e)}")
            raise

    def get_internal_links(self, url: str) -> List[str]:
        try:
            self._init_browser()
            context = self.browser.new_context(ignore_https_errors=True)
            time.sleep(5)
            page = context.new_page()
            page.goto(url, timeout=120000)  # Increased timeout for slow loading pages

            base_url = "/".join(url.split("/")[:3])
            links = page.query_selector_all("a[href]")
            all_links = []

            for link in links:
                href = self.safe_get_attribute(link, "href")
                if href:
                    full_url = urljoin(base_url, href)
                    # Get the full text content including nested elements
                    link_text = link.evaluate("node => node.textContent") or ""
                    link_text = " ".join(link_text.split())  # Clean up whitespace

                    if link_text and full_url.startswith(base_url):
                        all_links.append({"url": full_url, "text": link_text})

            page.close()
            context.close()
            return all_links

        except Exception as e:
            logger.error(f"Playwright link extraction failed: {str(e)}")
            raise

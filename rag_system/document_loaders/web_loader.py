import requests
from bs4 import BeautifulSoup
from .base_loader import BaseDocumentLoader


class WebDocumentLoader(BaseDocumentLoader):
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
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "Untitled"
        text = soup.get_text(separator="\n")
        return {
            "title": title,
            "text_content": text,
            "metadata": {"url": url, "file_type": "web"}
        }

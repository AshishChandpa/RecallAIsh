from abc import ABC, abstractmethod

class BaseDocumentLoader(ABC):
    @abstractmethod
    def load(self, source: str) -> dict:
        """
        Load a document from a given source (file path, URL, etc.) and return a dictionary with keys
        like 'title', 'text_content', and any additional metadata.
        """
        pass

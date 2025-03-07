from abc import ABC, abstractmethod
from typing import List


class BaseDocumentLoader(ABC):
    @abstractmethod
    def load(self) -> dict:
        """
        Load a document from a given source (file path, URL, etc.) and return a dictionary with keys
        like 'title', 'text_content', and any additional metadata.
        """
        raise NotImplemented("This method must be implemented in a subclass.")

    def loads(self, documents: List[str]) -> List[dict]:
        """
        Load multiple documents from a list of sources and return a list of dictionaries.
        """
        return [self.load(document) for document in documents]

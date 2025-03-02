from abc import ABC, abstractmethod


class BaseVectorStore(ABC):
    @abstractmethod
    def upsert(
            self,
            vectors: list,
            namespace: str
    ) -> None:
        """Upsert a batch of vectors into the vector store."""
        pass

    @abstractmethod
    def query(
            self,
            vector: list,
            top_k: int,
            filter: dict,
            namespace: str
    ) -> dict:
        """Query the vector store for the nearest neighbors."""
        pass

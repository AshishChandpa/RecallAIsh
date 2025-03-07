from pinecone import Pinecone

from .base import BaseVectorStore


class PineconeVectorStore(BaseVectorStore):
    def __init__(self, api_key: str, environment: str, index_name: str):
        """
        Initialize the Pinecone vector store.

        :param api_key: The Pinecone API key to use.
        :param environment: The Pinecone environment to use (e.g. "us").
        :param index_name: The name of the Pinecone index to use for the vector store.
        """
        pinecone = Pinecone(api_key=api_key, environment=environment)
        self.index = pinecone.Index(index_name)

    def upsert(self, vectors: list, namespace: str) -> None:
        """
        Upsert a batch of vectors into the Pinecone index.

        :param vectors: List of tuples (unique_id, embedding, metadata)
        :param namespace: The namespace to use for the upsert operation.
        """
        self.index.upsert(vectors=vectors, namespace=namespace)

    def query(self, vector: list, top_k: int, filter: dict, namespace: str) -> dict:
        """
        Query the Pinecone index for nearest vectors.

        :param vector: The query embedding.
        :param top_k: Number of top results to retrieve.
        :param filter: A dictionary filter (e.g. {"metadata.file_type": "pdf"}).
        :param namespace: The namespace to use for the query operation.
        :return: A dictionary with a "matches" key containing search results.
        """
        return self.index.query(
            vector=vector,
            top_k=top_k,
            filter=filter,
            include_metadata=True,
            namespace=namespace,
        )

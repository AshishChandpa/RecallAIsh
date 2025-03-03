from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from .base import BaseVectorStore


class QdrantVectorStore(BaseVectorStore):
    def __init__(
        self,
        collection_name: str,
        vector_size: int,
        host: str = None,
        port: int = None,
        url: str = None,
        distance: "Distance" = Distance.COSINE,
    ):
        """
        Initialize the Qdrant client and create a collection if it doesn't exist.

        :param host: The Qdrant server host.
        :param port: The Qdrant server port.
        :param collection_name: The collection name to use (acts as a namespace).
        :param vector_size: The size (dimension) of your embedding vectors.
        :param distance: The distance metric (default "Cosine").
        """
        if not url and (not host or not port):
            raise ValueError("Either 'url' or both 'host' and 'port' must be provided")

        if url:
            self.client = QdrantClient(url=url)
        else:
            self.client = QdrantClient(host=host, port=port)

        self.collection_name = collection_name
        self.vector_size = vector_size

        # Check if collection exists; if not, create it.
        existing_collections = [
            col.name for col in self.client.get_collections().collections
        ]
        if collection_name not in existing_collections:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=distance),
            )

    def upsert(self, vectors: list, namespace: str) -> None:
        """
        Upsert a batch of vectors into Qdrant.
        Note: The 'namespace' parameter is not used since Qdrant uses collections.

        :param vectors: List of tuples (unique_id, embedding, metadata)
        :param namespace: Ignored.
        """
        points = []
        for unique_id, embedding, metadata in vectors:
            points.append(PointStruct(id=unique_id, vector=embedding, payload=metadata))
        self.client.upsert(collection_name=self.collection_name, points=points)

    def query(self, vector: list, top_k: int, filter: dict, namespace: str) -> dict:
        """
        Query the Qdrant collection for nearest vectors.
        The provided filter is converted into Qdrant's filter format.

        :param vector: The query embedding.
        :param top_k: Number of top results to retrieve.
        :param filter: A dictionary filter (e.g. {"metadata.file_type": "pdf"}).
        :param namespace: Ignored.
        :return: A dictionary with a "matches" key containing search results.
        """
        # Convert a simple filter dictionary to Qdrant's format.
        if filter and len(filter) > 0:
            key, value = list(filter.items())[0]
            query_filter = {"must": [{"key": key, "match": {"value": value}}]}
        else:
            query_filter = None

        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=query_filter,
            limit=top_k,
            with_payload=True,
        )

        matches = []
        for point in search_result:
            match = {"id": point.id, "score": point.score, "metadata": point.payload}
            matches.append(match)
        return {"matches": matches}

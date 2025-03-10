from typing import Any, Mapping

from pymongo import MongoClient, operations

from .base import BaseVectorStore


class MongoDBVectorStore(BaseVectorStore):
    def __init__(
        self,
        url: str,
        database: str,
        collection_name: str,
        index_name: str,
        dimensions: int = 1536,
        similarity: str = "cosine",
    ):
        self.client = MongoClient(url)
        self.index_name = index_name
        self.db = self.client[database]
        self.collection = self.db[collection_name]
        if collection_name not in self.db.list_collection_names():
            self.db.create_collection(collection_name)
        self._create_vector_index(dimensions=dimensions, similarity=similarity)

    def _create_vector_index(self, dimensions: int, similarity: str):
        # Create the vector index with the specified dimensions and similarity metric
        try:
            index_result = self.collection.create_search_index(
                operations.SearchIndexModel(
                    definition={
                        "fields": [
                            {
                                "type": "vector",
                                "path": "embedding",
                                "numDimensions": dimensions,
                                "similarity": similarity,
                                "quantization": "scalar",
                            }
                        ]
                    },
                    name=self.index_name,
                    type="vectorSearch",
                )
            )
            print("Index creation result:", index_result)
            return index_result
        except Exception as e:
            print("Index may already exist or an error occurred:", e)

    def upsert(self, vectors: list, namespace: str) -> None:
        documents = [
            {"idx": idx, "embedding": vector, "metadata": metadata}
            for idx, vector, metadata in vectors
        ]
        self.collection.insert_many(documents)

    def query(self, vector: list, top_k: int, filter: dict, namespace: str) -> list[Mapping[str, Any] | Any]:
        vector_search_stage = {
            "$vectorSearch": {
                "index": self.index_name,
                "queryVector": vector,
                "numCandidates": max(top_k * 2, 10),  # Adjusting dynamically for better recall
                "path": "embedding",
                "limit": top_k,
            }
        }

        if filter:
            vector_search_stage["filter"] = filter  # Fixing incorrect curly braces

        pipeline = [
            vector_search_stage,
            {
                "$project": {
                    "_id": 0,
                    "text": 1,
                    "metadata": 1,
                    "score": {"$meta": "vectorSearchScore"},
                }
            },
        ]

        results = list(self.collection.aggregate(pipeline))

        print(f"Collection Indexes: {list(self.collection.list_search_indexes())}")

        return results

import uuid
from typing import List

from openai import OpenAI

from RecallAIsh.utils import chunk_text
from RecallAIsh.vector_store.base import BaseVectorStore


class RAGSystem:
    def __init__(
            self, vector_store: BaseVectorStore, vector_namespace: str, openai_api_key: str,
            embedding_model: str = "text-embedding-ada-002", base_url: str = None
    ):
        """
        Initialize a RAGSystem instance.

        :param vector_store: The vector store to use for storing and querying vectors.
        :param vector_namespace: The namespace to use for the vector store.
        :param openai_api_key: The OpenAI API key to use for embedding generation.
        """
        self.vector_store = vector_store
        self.vector_namespace = vector_namespace
        self.client = OpenAI(api_key=openai_api_key, base_url=base_url)
        self.embedding_model = embedding_model

    def get_embedding(self, text: str) -> list:
        """
        Compute an embedding for a given text string using OpenAI's text embeddings API.

        :param text: The text string to compute an embedding for.
        :param model: The model to use for computing the embedding (default: "text-embedding-ada-002").

        :return: A list of float32 values representing the embedding.
        """
        response = self.client.embeddings.create(input=[text], model=self.embedding_model)
        return response.data[0].embedding

    def create_embedding_and_upsert(self, document: dict) -> None:
        """
            Train the RAG system with a given document by chunking its content,
            generating embeddings for each chunk, and upserting them into the vector store.

            :param document: A dictionary containing the document's data with the following keys:
                - title: The title of the document.
                - text_content: The main text content of the document.
                - metadata: Additional metadata associated with the document.
            :return: None
        """
        if type(document) is list:
            for doc in document:
                self.create_embedding_and_upsert(doc)
        title = document.get("title", "Untitled")

        text_content = document.get("text_content", "")

        full_text = f"Title: {title}\n\nContent: {text_content}"

        chunks = chunk_text(full_text)

        for chunk_idx, chunk in enumerate(chunks):
            embedding = self.get_embedding(chunk)

            unique_chunk_id = f"{str(uuid.uuid4())}"

            metadata = {
                "title": title,
                "chunk_text": chunk,
                "chunk_index": chunk_idx,
                "metadata": document.get("metadata", {}),
            }

            self.vector_store.upsert(
                vectors=[(unique_chunk_id, embedding, metadata)],
                namespace=self.vector_namespace,
            )

    def retrieve_documents(
            self, user_query: str, filter_value: str, top_k: int = 5
    ) -> str:
        """
        Query the RAG system and retrieve the top-k relevant context from the database.

        :param user_query: The user's query string.
        :param filter_value: The value to filter by in the metadata dictionary.
        :param top_k: The number of top results to retrieve (default: 5).
        :return: The retrieved context as a string.
        """
        query_embedding = self.get_embedding(user_query)

        results = self.vector_store.query(
            vector=query_embedding,
            top_k=top_k,
            filter={"metadata.file_type": filter_value},
            namespace=self.vector_namespace,
        )

        results_list = (
            results if isinstance(results, list) else results.get("matches", [])
        )
        retrieved_context = "\n\n".join(
            match["metadata"]["chunk_text"] for match in results_list
        )

        return retrieved_context

    def ingestion_pipeline(self, documents: List) -> None:
        """
        Ingest a list of documents into the RAG system by creating embeddings and upserting them into the vector store.
        """
        for doc in documents:
            self.create_embedding_and_upsert(doc)

    def chat(self, full_prompt, model, temperature=0.7, max_tokens=500):
        """
        Send a full prompt to the OpenAI chat API and return the response.

        :param full_prompt: The full prompt to send to the chat API.
        :param model: The model to use for generating a response.
        :param temperature: The temperature to use for generating a response (default: 0.7).
        :param max_tokens: The maximum number of tokens to generate in the response (default: 500).

        :return: The response from the chat API.
        """
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

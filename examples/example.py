import os

from dotenv import load_dotenv
from openai import OpenAI

from rag_system.prompt_manager import PromptManager
from rag_system.rag_system import RAGSystem
from rag_system.vector_store.qdrant_store import QdrantVectorStore

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def main():
    """
    Example script to demonstrate the usage of the RAG system.
    """
    # Configure Qdrant connection (adjust host, port, and collection details as needed)
    qdrant_store = QdrantVectorStore(
        url="http://localhost:6333",
        collection_name="my_rag_collection",
        vector_size=1536,  # adjust to your embedding dimension
    )

    # Initialize the RAG system with Qdrant.
    rag_system = RAGSystem(
        vector_store=qdrant_store,
        vector_namespace="unused_namespace",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )

    # # Ingest PDFs and websites
    pdfs = ["/path/to/pdf"]
    websites = ["https://xyz.com/"]
    rag_system.ingestion_pipeline(pdfs=pdfs, websites=websites)

    # Create a Prompt::
    user_query = "Explain the main concepts from the documents."
    context = rag_system.retrieve_documents(user_query, "pdf")

    instructions = "You are an expert assistant tasked with answering questions using the provided context."
    prompt_manager = PromptManager(instructions=instructions)
    full_prompt = prompt_manager.create_prompt(context, user_query)
    print("Full Prompt:\n", full_prompt)

    answer = rag_system.chat(full_prompt, "gpt-4o-mini")
    print("Answer:", answer)


if __name__ == "__main__":
    main()

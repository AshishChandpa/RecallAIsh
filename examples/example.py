import os

from dotenv import load_dotenv
from openai import OpenAI

from RecallAIsh.prompt_manager import PromptManager
from RecallAIsh.rag_system import RAGSystem
from RecallAIsh.vector_store.mongodb_store import MongoDBVectorStore
from RecallAIsh.enums import ScrapperType

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def main():
    """
    Example script to demonstrate the usage of the RAG system.
    """
    # Configure Qdrant connection (adjust host, port, and collection details as needed)

    mongo_store = MongoDBVectorStore(
        url="<MongoURL>",
        database="vectorstore",
        collection_name="my_rag_collection",
        index_name="my_vector_index",
    )
    # Initialize the RAG system with Qdrant.
    rag_system = RAGSystem(
        vector_store=mongo_store,
        vector_namespace="unused_namespace",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )
    # Ingest PDFs and websites
    pdfs = ["file"]
    websites = ["https://www.example.com"]
    from RecallAIsh.document_loaders.pdf_loader import PdfDocumentLoader
    from RecallAIsh.document_loaders.web_loader import WebDocumentLoader

    rag_system.ingestion_pipeline(
        documents=[PdfDocumentLoader().loads(pdfs), WebDocumentLoader(scraper_type=ScrapperType.PLAYWRIGHT.value).loads(websites)]
    )

    # # Create a Prompt::
    user_query = "What did he think about programming?"
    context = rag_system.retrieve_documents(user_query, "pdf")

    instructions = "You are an expert assistant tasked with answering questions using the provided context."
    prompt_manager = PromptManager(instructions=instructions)
    full_prompt = prompt_manager.create_prompt(context, user_query)
    print("Full Prompt:\n", full_prompt)

    answer = rag_system.chat(full_prompt, "gpt-4o-mini")
    print("Answer:", answer)


if __name__ == "__main__":
    main()

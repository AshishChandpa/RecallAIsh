from RecallAIsh.prompt_manager import PromptManager
from RecallAIsh.rag_system import RAGSystem
from RecallAIsh.utils import chunk_text
from RecallAIsh.vector_store.base import BaseVectorStore


def test_chunk_text():
    text = "This is a sample text to be chunked into smaller pieces."
    chunks = chunk_text(text, chunk_size=5, chunk_overlap=2)
    assert len(chunks) > 0
    assert all(isinstance(chunk, str) for chunk in chunks)


def test_prompt_manager():
    instructions = "Provide a detailed answer."
    context = "This is the context."
    query = "What is the context?"
    prompt_manager = PromptManager(instructions)
    prompt = prompt_manager.create_prompt(context, query)
    assert instructions in prompt
    assert context in prompt
    assert query in prompt


class MockVectorStore(BaseVectorStore):
    def upsert(self, vectors: list, namespace: str) -> None:
        pass

    def query(self, vector: list, top_k: int, filter: dict, namespace: str) -> dict:
        return {"matches": [{"metadata": {"chunk_text": "sample text"}}]}


def test_rag_system():
    vector_store = MockVectorStore()
    rag_system = RAGSystem(vector_store, "namespace", "fake_api_key")
    document = {"title": "Test", "text_content": "This is a test document."}
    rag_system.create_embedding_and_upsert(document)
    context = rag_system.retrieve_documents("test query", "pdf")
    assert "sample text" in context


def test_example():
    assert True

# RecallAI

## Overview
RecallAI is a powerful Retrieval-Augmented Generation (RAG) framework designed to enhance the capabilities of Large Language Models (LLMs). It integrates real-time knowledge retrieval from structured and unstructured data sources, enabling more informed and accurate responses.

## Features
- **Retrieval-Augmented Generation (RAG):** Enhances LLM responses with real-time information retrieval.
- **Integration with OpenAI Models:** Supports GPT-based models for improved text generation.
- **Qdrant Vector Store:** Efficient vector storage and retrieval for document embeddings.
- **Document & Web Ingestion:** Supports ingesting PDFs and web pages for knowledge retrieval.

## Installation
### Prerequisites
- Python 3.10+
- pip package manager
- [Qdrant](https://qdrant.tech/) or [Pinecone](https://www.pinecone.io/) vector database
- OpenAI API Key

### Install via PyPI
You can install RecallAI directly from PyPI:
```sh
pip install recall-ai
```

### Manual Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/AshishChandpa/RecallAI.git
   cd RecallAI
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Create a `.env` file in the project root.
   - Add your OpenAI API key:
     ```sh
     OPENAI_API_KEY=your_openai_api_key
     ```
4. Ensure Qdrant is running:
   ```sh
   docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
   ```

## Usage
### Running the Example Script
Execute the script to see the RAG system in action:
```sh
python examples/example.py
```

### Using RecallAI in Your Project
Import and use RecallAI in your Python scripts:
```python
from recallai import RAGSystem, QdrantVectorStore, PromptManager

# Configure Qdrant connection
qdrant_store = QdrantVectorStore(
    url="http://localhost:6333",
    collection_name="my_rag_collection",
    vector_size=1536,  # adjust to your embedding dimension
)

# Initialize the RAG system
rag_system = RAGSystem(
    vector_store=qdrant_store,
    vector_namespace="<NameSpaceName>",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

# Retrieve documents and generate responses
user_query = "Explain the main concepts from the documents."
context = rag_system.retrieve_documents(user_query, "pdf")

instructions = "You are an expert assistant tasked with answering questions using the provided context."
prompt_manager = PromptManager(instructions=instructions)
full_prompt = prompt_manager.create_prompt(context, user_query)

answer = rag_system.chat(full_prompt, "gpt-4o-mini")
print("Answer:", answer)
```

## Configuration
- Adjust the `QdrantVectorStore` parameters for different vector dimensions or collection names.
- Modify the ingestion pipeline to include additional document sources.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For questions or suggestions, reach out via [email](mailto:chandpa.ashish007@gmail.com).


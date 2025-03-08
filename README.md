# RecallAIsh: A Retrieval-Augmented Generation (RAG) Framework

RecallAIsh is a comprehensive Python package designed to easily add Retrieval-Augmented Generation capabilities to your applications. It seamlessly integrates real-time knowledge retrieval with Large Language Model (LLM) responses to deliver context-aware, accurate, and dynamic results.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Web Scraper Integration](#web-scraper-integration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview
RecallAIsh leverages the power of state-of-the-art retrieval methods combined with LLMs, allowing you to enrich your text generation workflows with up-to-date and contextually relevant information. With built-in support for various document sources, dynamic web content scraping, and flexible vector storage solutions such as Qdrant, Pinecone, and MongoDB, this package is ideal for projects ranging from smart document QA systems to advanced conversational agents.

## Features
- **Retrieval-Augmented Generation (RAG):** Combine real-time data retrieval with LLM responses for informed outputs.
- **Plug-and-Play Integration:** Easily integrate with GPT-based models and other LLMs for powerful natural language understanding.
- **Vector Storage Solutions:** Built-in support for Qdrant, Pinecone, and MongoDB for efficient document embedding storage and retrieval.
- **Multi-Source Ingestion:** Ingest content from PDFs, web pages via integrated web scrapers, and additional document sources.
- **Custom Prompt Management:** Create tailored prompts with context-rich information to steer LLM responses.
- **Modular Pipeline:** Extend or modify components according to your project requirements.

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- A vector database: [Qdrant](https://qdrant.tech/), [Pinecone](https://www.pinecone.io/), or [MongoDB](https://www.mongodb.com/)
- An OpenAI API key

### Install via PyPI
Install RecallAIsh using the Python Package Index:
```sh
pip install RecallAIsh
```
If you plan to use MongoDB for storing vectors, install the optional dependencies:
```sh
pip install RecallAIsh[mongodb]
```

### Manual Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/AshishChandpa/RecallAIsh.git
   cd RecallAIsh
   ```
2. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your OpenAI API key:
   ```sh
   OPENAI_API_KEY=your_openai_api_key
   ```
4. Ensure your vector database is up and running. For example, start Qdrant:
   ```sh
   docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
   ```
   Or, set up your MongoDB instance accordingly.

## Usage

### Running an Example
See RecallAIsh in action with the provided example script:
```sh
python examples/example.py
```

### Integrating RecallAIsh into Your Project
Below is a detailed example highlighting primary components, including the new MongoDB vector store and web scraper integration:

```python
import os

from RecallAIsh.document_loaders.web_loader import WebDocumentLoader
from RecallAIsh.prompt_manager import PromptManager
from RecallAIsh.rag_system import RAGSystem
from RecallAIsh.vector_store.mongodb_store import MongoDBVectorStore
from RecallAIsh.vector_store.qdrant_store import QdrantVectorStore

# Example: Connecting using Qdrant
qdrant_store = QdrantVectorStore(
    url="http://localhost:6333",
    collection_name="my_rag_collection",
    vector_size=1536,  # Adjust to match your chosen embedding dimension
)

# Example: Connecting using MongoDB
mongodb_store = MongoDBVectorStore(
    uri="<MongoAtlasURL>",
    database="recallai_db",
    collection="vector_store",
    vector_size=1536,  # Adjust to match your embedding dimension
)

# Initialize the Retrieval-Augmented Generation system with your preferred vector store
rag_system = RAGSystem(
    vector_store=mongodb_store,  # or qdrant_store if preferred
    vector_namespace="default_namespace",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

# Retrieve relevant documents based on the user's query
user_query = "Summarize the latest news on technology."
# First, use the web scraper to fetch dynamic content from the web
doc = WebDocumentLoader().load(url="https://news.example.com/technology")
# Store processed web content into the vector store as needed
rag_system.ingestion_pipeline([doc])

# Retrieve documents including the freshly scraped web content
context = rag_system.retrieve_documents(user_query, source="all")

# Define custom instructions and generate the full prompt
instructions = "You are an expert assistant tasked with summarizing complex technical news."
prompt_manager = PromptManager(instructions=instructions)
full_prompt = prompt_manager.create_prompt(context, user_query)

# Generate answer using the RAG system
response = rag_system.chat(full_prompt, model="gpt-4o-mini")
print("Answer:", response)
```

## Configuration
- Customize vector store parameters such as collection name and embedding dimensions as needed.
- Extend the ingestion pipeline to incorporate additional document formats, web scraping, or data sources.
- Adjust the prompt management module to refine how context and instructions are combined for your specific application.

## Web Scraper Integration
RecallAIsh now includes a web scraper module which leverages standard libraries like BeautifulSoup and requests. This allows you to dynamically ingest web content:
- Configure the scraper with custom parameters such as user-agent, timeout, and parsing criteria.
- Automatically process and clean HTML content before storing it in your chosen vector store.

## Contributing
Contributions are welcome! To contribute:
1. Open an issue for discussion or report a bug.
2. Submit a pull request with your improvements.
3. Follow the coding standards and ensure tests pass before submission.

## License
RecallAIsh is available under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact
For further questions or feedback, please contact via email: [chandpa.ashish007@gmail.com](mailto:chandpa.ashish007@gmail.com).

Happy coding with RecallAIsh!

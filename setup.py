from os import path

from setuptools import find_packages, setup

work_dir = path.abspath(path.dirname(__file__))

with open(path.join(work_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="RecallAIsh",
    version="0.2.4",
    packages=find_packages(),
    install_requires=[
        "openai",
        "beautifulsoup4",
        "requests",
        "PyPDF2",
        "pymongo",
        "pinecone-client",
        "qdrant-client",
        "playwright"
    ],
    extras_require={
        "pinecone": ["pinecone-client"],
        "qdrant": ["qdrant-client"],
        "mongodb": ["pymongo"],
        "playwright": ["playwright"],
    },
    author="Ashish Chandpa",
    author_email="chandpa.ashish007@gmail.com",
    description=(
        "RecallAI is a cutting-edge Retrieval-Augmented Generation (RAG) framework "
        "designed for Large Language Models (LLMs). It enhances LLM responses by integrating "
        "real-time knowledge retrieval from structured and unstructured data sources."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AshishChandpa/RecallAI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)

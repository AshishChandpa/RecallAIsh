from setuptools import setup, find_packages
from os import path

work_dir = path.abspath(path.dirname(__file__))

with open(path.join(work_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="RecallAI",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "pinecone-client",
        "qdrant-client",
        "beautifulsoup4",
        "requests",
        "PyPDF2",
    ],
    author="Ashish Chandpa",
    author_email="chandpa.ashish007@gmail.com",
    description="RecallAI is a cutting-edge Retrieval-Augmented Generation (RAG) framework designed for Large Language Models (LLMs). It enhances LLM responses by integrating real-time knowledge retrieval from structured and unstructured data sources.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AshishChandpa/RecallAI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)

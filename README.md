# Code-RAG: Chroma Vector Database with Anything LLM

This repository contains instructions for creating a Code Retrieval-Augmented Generation (RAG) system with Chroma DB and Anything LLM.

## 📋 Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Code Indexing](#code-indexing)
- [Starting the Chroma Server](#starting-the-chroma-server)
- [Setting Up Anything LLM](#setting-up-anything-llm)
- [Troubleshooting](#troubleshooting)

## 🔍 Overview

This system enables indexing of your own codebases and making intelligent queries using LLMs (Large Language Models). The key components are:

1. **Chroma**: A vector database for storing code embeddings
2. **Anything LLM**: A user-friendly chat interface for querying codebases
3. **LangChain**: Framework for integrating vector databases with LLMs

## 🛠️ Installation

### Prerequisites

- Python 3.8+ and pip
- OpenAI API key (for embeddings and optionally for the LLM)
- Optional: Anthropic API key (for Claude models)

### Install Packages

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install chromadb langchain langchain-community langchain-openai python-dotenv
```

### Create .env File

Create a `.env` file in the project directory with API keys:

```
OPENAI_API_KEY=your-openai-api-key-here
```

## 📚 Code Indexing

Use the `chroma_indexer.py` script to index your codebases. Key options:

### Index a New Codebase

```bash
python chroma_indexer.py --path /path/to/your/codebase --collection my_collection
```

### Add Another Codebase to the Same Collection

```bash
python chroma_indexer.py --path /path/to/another/codebase --collection my_collection --add
```

### Customize Indexed File Types

```bash
python chroma_indexer.py --path /path/to/codebase --collection my_collection --extensions .py,.js,.html,.ts,.jsx
```

### Customize Database Storage Location

```bash
python chroma_indexer.py --path /path/to/codebase --collection my_collection --persist-dir /path/to/chroma_db
```

## 🖥️ Starting the Chroma Server

After indexing, you need to start the Chroma server to access the vector database:

```bash
chroma run --path /path/to/chroma_db --host 0.0.0.0 --port 8000
```

The server will then be accessible at http://localhost:8000.

## 🤖 Setting Up Anything LLM

[Anything LLM](https://anythingllm.com/) is a user-friendly chat interface that can work with your Chroma index.

### Installing Anything LLM

1. Download Anything LLM from https://anythingllm.com/
2. Install it according to the instructions
3. Start Anything LLM

### Configuring Anything LLM

1. Open Anything LLM
2. Create a new workspace or select an existing one
3. Navigate to workspace settings

4. Configure the vector database:
   - Select "Chroma" as the vector database type
   - Server URL: e.g., `http://localhost:8000`
   - **VERY IMPORTANT**: Collection Name: Your collection name (e.g., `my_collection`) MUST ALWAYS be the SAME as the workspace name in Anything!

5. Configure the Embedding Provider:
   - Select "OpenAI" as the embedding provider
   - Enter your OpenAI API key
   - **IMPORTANT**: Use the **SAME** embedding provider as during indexing!

6. Configure the LLM:
   - Choose an LLM provider (OpenAI, Anthropic, etc.)
   - Select a model (GPT-4, Claude 3, etc.)
   - Enter the corresponding API key

7. Save the settings

## ❓ Troubleshooting

### Collection Not Found

If you receive a "Collection XYZ does not exist" error:

1. Check available collections:
   ```python
   import chromadb
   client = chromadb.HttpClient(host="localhost", port=8000)
   print(client.list_collections())
   ```

2. Ensure the collection name in Anything LLM exactly matches the actual collection name (mind uppercase/lowercase)

3. Verify that the workspace name is exactly the same as your collection. Otherwise, Anything LLM cannot access your collection.

### Embedding Dimension Error

If errors occur with "Embedding dimension X does not match collection dimensionality Y":

1. Ensure you use the same embedding provider in Anything LLM as during indexing (here OpenAI)
2. Check that the correct embedding model is selected (OpenAI uses 1536 dimensions)

### Other Issues

- Ensure the Chroma server is running and accessible with no console errors
- Verify that API keys are correct and valid
- For problems with existing collections, create a new collection if necessary
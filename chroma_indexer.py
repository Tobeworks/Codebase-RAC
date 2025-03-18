import chromadb
import os
import argparse
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

#########################################################################
# CONFIGURATION - These constants can be easily adjusted
#########################################################################

# Default path to your code repository
DEFAULT_CODE_PATH = "/Users/tobe/Sites/mycodebase/"

# Default collection name
DEFAULT_COLLECTION_NAME = "code_collection"

# Default path to your Chroma database
DEFAULT_PERSIST_DIR = "/Users/tobe/Sites/python/langchain_chroma/chroma_db"

# Default file extensions to index (comma-separated)
DEFAULT_FILE_EXTENSIONS = ".py,.js,.html,.css,.vue,.jsx,.tsx,.md,.txt"

# Default chunk size for text splitting
DEFAULT_CHUNK_SIZE = 1000

# Default chunk overlap for text splitting
DEFAULT_CHUNK_OVERLAP = 200

# Directories to ignore
EXCLUDE_DIRS = {
    'node_modules', '.git', 'dist', 'build', 'old',
    'lib', 'libs', 'venv', '.venv', 'env',
    '.env', '__pycache__', 'egg-info',
    '.pytest_cache', '.mypy_cache', '.coverage',
    'htmlcov', '.tox', '.eggs'
}

# Files to ignore
EXCLUDE_FILES = {
    '.DS_Store', 'Thumbs.db', '.gitignore',
    'package-lock.json', 'yarn.lock', '.env',
    '.editorconfig', '.prettierrc', '.eslintrc'
}

# Separators for text splitting
SEPARATORS = ["\nclass ", "\ndef ", "\nfunction ", "\n\n", "\n", " ", ""]

# Load environment variables
load_dotenv()

def load_documents(folder_path, text_extensions):
    documents = []
    
    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if file in EXCLUDE_FILES:
                continue
                
            file_path = os.path.join(root, file)
            
            if any(file.endswith(ext) for ext in text_extensions):
                try:
                    loader = TextLoader(file_path)
                    docs = loader.load()
                    
                    for doc in docs:
                        doc.metadata["file_path"] = file_path
                        doc.metadata["relative_path"] = os.path.relpath(file_path, folder_path)
                        doc.metadata["file_name"] = file
                        doc.metadata["source_repo"] = os.path.basename(folder_path)
                        doc.metadata["project"] = os.path.basename(folder_path)
                        
                    documents.extend(docs)
                    print(f"Loaded: {file_path}")
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
                    
    return documents

def index_new_codebase(folder_path, collection_name, persist_directory, text_extensions, chunk_size, chunk_overlap):
    client = chromadb.PersistentClient(path=persist_directory)
    
    existing_collections = client.list_collections()
    if collection_name in existing_collections:
        print(f"Collection '{collection_name}' already exists and will be deleted.")
        client.delete_collection(collection_name)
    
    print(f"Creating new collection: {collection_name}")
    collection = client.create_collection(
        name=collection_name,
        metadata={"description": f"Code documents from the {collection_name} project"}
    )
    
    print(f"Loading documents from: {folder_path}")
    documents = load_documents(folder_path, text_extensions)
    print(f"Number of loaded documents: {len(documents)}")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=SEPARATORS
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Number of chunks: {len(chunks)}")
    
    print("Creating embeddings with OpenAI...")
    embeddings = OpenAIEmbeddings()
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=persist_directory
    )
    
    print("Indexing complete!")
    print(f"Collection '{collection_name}' was successfully created with {len(chunks)} documents.")

def add_to_existing_collection(folder_path, collection_name, persist_directory, text_extensions, chunk_size, chunk_overlap):
    client = chromadb.PersistentClient(path=persist_directory)
    existing_collections = client.list_collections()
    
    if collection_name not in existing_collections:
        print(f"Collection '{collection_name}' does not exist. Creating a new one.")
        index_new_codebase(folder_path, collection_name, persist_directory, text_extensions, chunk_size, chunk_overlap)
        return
    
    print(f"Loading additional documents from: {folder_path}")
    documents = load_documents(folder_path, text_extensions)
    print(f"Number of loaded documents: {len(documents)}")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=SEPARATORS
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Number of new chunks: {len(chunks)}")
    
    print("Creating embeddings with OpenAI...")
    embeddings = OpenAIEmbeddings()
    
    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_directory
    )
    
    vectorstore.add_documents(chunks)
    
    print("Addition complete!")
    
    count = client.get_collection(collection_name).count()
    print(f"Collection '{collection_name}' now contains a total of {count} documents.")

def main():
    parser = argparse.ArgumentParser(description='Index code repositories in Chroma')
    parser.add_argument('--path', type=str, default=DEFAULT_CODE_PATH, 
                        help=f'Path to code repository (default: {DEFAULT_CODE_PATH})')
    parser.add_argument('--collection', type=str, default=DEFAULT_COLLECTION_NAME, 
                        help=f'Name of the collection (default: {DEFAULT_COLLECTION_NAME})')
    parser.add_argument('--persist-dir', type=str, default=DEFAULT_PERSIST_DIR, 
                        help=f'Directory for the Chroma database (default: {DEFAULT_PERSIST_DIR})')
    parser.add_argument('--add', action='store_true', 
                        help='Add to existing collection instead of replacing it')
    parser.add_argument('--extensions', type=str, default=DEFAULT_FILE_EXTENSIONS,
                        help=f'Comma-separated list of file extensions (default: {DEFAULT_FILE_EXTENSIONS})')
    parser.add_argument('--chunk-size', type=int, default=DEFAULT_CHUNK_SIZE, 
                        help=f'Size of chunks (default: {DEFAULT_CHUNK_SIZE})')
    parser.add_argument('--chunk-overlap', type=int, default=DEFAULT_CHUNK_OVERLAP, 
                        help=f'Overlap of chunks (default: {DEFAULT_CHUNK_OVERLAP})')
    
    args = parser.parse_args()
    
    extensions = args.extensions.split(',')
    
    if args.add:
        add_to_existing_collection(args.path, args.collection, args.persist_dir, extensions, 
                                 args.chunk_size, args.chunk_overlap)
    else:
        index_new_codebase(args.path, args.collection, args.persist_dir, extensions,
                         args.chunk_size, args.chunk_overlap)
    
    print("\nInstructions for Anything LLM:")
    print("1. Start the Chroma server with:")
    print(f"   chroma run --path {args.persist_dir} --host 0.0.0.0 --port 8000")
    print("2. Configure Anything LLM:")
    print("   - Server: http://localhost:8000")
    print(f"   - Collection: {args.collection}")
    print("   - IMPORTANT: Use OpenAI for embeddings")

if __name__ == "__main__":
    main()
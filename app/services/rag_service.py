from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore as Qdrant
import os

embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "rag_documents"

def process_and_store_document(file_path: str):
    
    print(f"[RAG Service] Loading file: {file_path}")
    
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError("Unsupported file format. Only PDF and TXT are supported.")

    documents = loader.load()

    print("[RAG Service] ✂️ Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, # حجم القطعة الواحدة
        chunk_overlap=50 
    )
    chunks = text_splitter.split_documents(documents)
    print(f"[RAG Service] ✅Created {len(chunks)} chunks.")

    print("[RAG Service]  Generating embeddings and storing in Qdrant...")
    Qdrant.from_documents(
        chunks,
        embeddings_model,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME,
    )
    print("[RAG Service]  Successfully stored in Vector DB!")
    return True
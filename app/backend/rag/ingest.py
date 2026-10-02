from langchain_community.document_loaders import DirectoryLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_core.documents import Document
import uuid
import json,os
load_dotenv()

from app.backend.config import (COLLECTION_NAME,EMBEDDING_MODEL,CHUNK_OVERLAP,CHUNK_SIZE,QDRANT_URL,BM25_FILE)

#embeddings
embeddings=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

#splitter
text_splitter=RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,chunk_overlap=CHUNK_OVERLAP)

client = QdrantClient(url=QDRANT_URL)

def save_chunk_for_bm25(chunks):
    """Overwrite BM25 storage with the supplied chunks."""
    data = []
    for doc in chunks:
        data.append({
            "page_content": doc.page_content,
            "metadata": doc.metadata,
        })
    with open(BM25_FILE, "w") as f:
        json.dump(data, f, indent=4)

def append_chunks_for_bm25(chunks):
    """Append new chunks to existing BM25 storage."""

    data = []

    if os.path.exists(BM25_FILE):
        with open(BM25_FILE, "r", ) as f:
            data = json.load(f)

    for doc in chunks:
        data.append({
            "page_content": doc.page_content,
            "metadata": doc.metadata,
        })

    with open(BM25_FILE, "w" ) as f:
        json.dump(data,f,indent=4,ensure_ascii=False)



def load_chunks_for_bm25():
    """Load chunks from BM25 JSON storage."""
    if not os.path.exists(BM25_FILE):
        return []
    
    with open(BM25_FILE, "r") as f:
        data = json.load(f)
        return [Document(page_content=item['page_content'],metadata=item['metadata']) for item in data]


def ingest():
    """Load, split, embed and save documents"""

    #document loader
    loader=DirectoryLoader("app/data",glob="*.txt",loader_cls=TextLoader)
    documents=loader.load()

    chunks=text_splitter.split_documents(documents)
    for doc in chunks:
        doc.metadata["chunk_id"] = str(uuid.uuid4())

    # Save chunks for BM25
    save_chunk_for_bm25(chunks)

    #create vector store
    vector_store=QdrantVectorStore.from_documents(documents=chunks,embedding=embeddings,url=QDRANT_URL,collection_name=COLLECTION_NAME)
    print(f"Chunk: {len(chunks)}")

def add_new_document(file_path):
    """Add only a new document to existing vector store."""

    # Load ONLY the new document
    loader=TextLoader(file_path)
    documents=loader.load()

    # Split ONLY the new document
    chunks=text_splitter.split_documents(documents)

    for doc in chunks:
        doc.metadata['chunk_id']=str(uuid.uuid4())
        doc.metadata["source"] = file_path

    # Save chunks for BM25
    append_chunks_for_bm25(chunks)

    vector_store=QdrantVectorStore(client=client,collection_name=COLLECTION_NAME,embedding=embeddings)

    # Embed and add ONLY new chunks
    vector_store.add_documents(chunks)

    print(f"Added {len(chunks)} new chunks")


if __name__=="__main__":
    ingest()
    # add_new_document('app/data/10_learning_and_development.txt')
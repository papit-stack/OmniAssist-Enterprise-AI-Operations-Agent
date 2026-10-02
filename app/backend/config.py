EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L6-v2"

VECTOR_STORE_PATH = "./vector_db_faiss"

COLLECTION_NAME = "documents"

QDRANT_URL = "http://localhost:6333"


CHUNK_SIZE=1000
CHUNK_OVERLAP=50


COHERE_RERANK_MODEL='rerank-v3.5'

GEMINI_MODEL='gemini-3.5-flash-lite'
MODEL_PROVIDER="google_genai"

GROQ_MODEL='openai/gpt-oss-120b'
GROQ_MODEL_PROVIDER='groq'

BM25_FILE="bm25_chunks.json"
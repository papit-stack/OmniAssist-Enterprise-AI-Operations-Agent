from app.backend.config import (COLLECTION_NAME,EMBEDDING_MODEL,COHERE_RERANK_MODEL, QDRANT_URL)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever,ContextualCompressionRetriever
from app.backend.rag.ingest import load_chunks_for_bm25
from langchain_cohere import CohereRerank
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()


client=QdrantClient(url=QDRANT_URL)

embeddings=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
vector_store=QdrantVectorStore(client=client,collection_name=COLLECTION_NAME,embedding=embeddings)
chunks=load_chunks_for_bm25()

#retriever
vector_retriever=vector_store.as_retriever(search_kwargs={'k':10})
bm25_retriever=BM25Retriever.from_documents(chunks)
bm25_retriever.k=10

#hybrid retriever
hybrid_retriever=EnsembleRetriever(retrievers=[vector_retriever,bm25_retriever],weights=[0.7, 0.3])
reranker=CohereRerank(model=COHERE_RERANK_MODEL,top_n=5)
retriever=ContextualCompressionRetriever(base_retriever=hybrid_retriever,base_compressor=reranker)

def use_retriever(query:str):
    docs = retriever.invoke(query)

    context_parts = []
    metadata = []

    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source")

        context_parts.append(
            f"[{i}] Source: {source or 'Unknown'}\n"
            f"{doc.page_content}"
        )

        metadata.append({
            "citation": i,
            "source": source,
            "chunk_id": doc.metadata.get("chunk_id")
        })

    context = "\n\n".join(context_parts)

    return context, metadata





if __name__=="__main__":
    context, metadata = use_retriever(
        "what are types of leave policy"
    )

    print("CONTEXT:")
    print(context)

    print("METADATA:")
    for item in metadata:
        print(item)

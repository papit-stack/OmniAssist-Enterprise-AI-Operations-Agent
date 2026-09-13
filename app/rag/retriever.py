from langchain_community.vectorstores import FAISS
from app.config import (VECTOR_STORE_PATH,EMBEDDING_MODEL,COHERE_RERANK_MODEL)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever,ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from dotenv import load_dotenv
load_dotenv()

embeddings=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
vector_store=FAISS.load_local(VECTOR_STORE_PATH,embeddings=embeddings,allow_dangerous_deserialization=True)
chunks=list(vector_store.docstore._dict.values())

#retriever
vector_retriever=vector_store.as_retriever(search_kwargs={'k':10})
bm25_retriever=BM25Retriever.from_documents(chunks)
bm25_retriever.k=10

#hybrid retriever
hybrid_retriever=EnsembleRetriever(retrievers=[vector_retriever,bm25_retriever],weights=[0.7, 0.3])
reranker=CohereRerank(model=COHERE_RERANK_MODEL,top_n=5)
retriever=ContextualCompressionRetriever(base_retriever=hybrid_retriever,base_compressor=reranker)

def use_retriever(query:str):
    result=retriever.invoke(query)
    context="\n\n".join(doc.page_content for doc in result)
    metadata=[doc.metadata for doc in result]
    return context,metadata

if __name__=="__main__":
    context, metadata = use_retriever(
        "what are types of leave policy"
    )

    print("CONTEXT:")
    print(context)

    print("METADATA:")
    for item in metadata:
        print(item)



from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from app.config import (VECTOR_STORE_PATH,EMBEDDING_MODEL,CHUNK_OVERLAP,CHUNK_SIZE)

load_dotenv()


#embeddings
embeddings=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def ingest():
    """Load, split, embed and save documents"""
    #document loader
    loader=DirectoryLoader("app/data",glob="*.txt",loader_cls=TextLoader)
    documents=loader.load()

    #splitter
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,chunk_overlap=CHUNK_OVERLAP)
    chunks=text_splitter.split_documents(documents)
    for idx,doc in enumerate(chunks):
        doc.metadata['chunk_id']=idx


    #create vector store
    vector_store=FAISS.from_documents(chunks,embedding=embeddings)
    vector_store.save_local(VECTOR_STORE_PATH)
    print(f"Chunk: {len(chunks)}")
    print(f"Vector store saved at: {VECTOR_STORE_PATH}")

if __name__=="__main__":
    ingest()
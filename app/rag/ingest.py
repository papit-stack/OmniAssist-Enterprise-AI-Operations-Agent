from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from app.config import (VECTOR_STORE_PATH,EMBEDDING_MODEL,CHUNK_OVERLAP,CHUNK_SIZE)

load_dotenv()


#embeddings
embeddings=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
#splitter
text_splitter=RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,chunk_overlap=CHUNK_OVERLAP)

def ingest():
    """Load, split, embed and save documents"""

    #document loader
    loader=DirectoryLoader("app/data",glob="*.txt",loader_cls=TextLoader)
    documents=loader.load()

    chunks=text_splitter.split_documents(documents)
    for idx,doc in enumerate(chunks):
        doc.metadata['chunk_id']=idx


    #create vector store
    vector_store=FAISS.from_documents(chunks,embedding=embeddings)
    vector_store.save_local(VECTOR_STORE_PATH)
    print(f"Chunk: {len(chunks)}")
    print(f"Vector store saved at: {VECTOR_STORE_PATH}")

def add_new_document(file_path):
    """Add only a new document to existing vector store."""

    # Load ONLY the new document
    loader=TextLoader(file_path)
    documents=loader.load()

    # Split ONLY the new document
    chunks=text_splitter.split_documents(documents)

    vector_store=FAISS.load_local(VECTOR_STORE_PATH,embeddings,allow_dangerous_deserialization=True)

    old_chunk=list(vector_store.docstore._dict.values())

    for idx,doc in enumerate(chunks):
        print(f"Document: {idx}")
        doc.metadata['chunk_id']=len(old_chunk)+idx
        doc.metadata["source"] = file_path
        # print(doc,"\n")

    # print(old_chunk)
    # Embed and add ONLY new chunks
    vector_store.add_documents(chunks)

    # Save updated vector store
    vector_store.save_local(VECTOR_STORE_PATH)
    
    print(f"Added {len(chunks)} new chunks")


if __name__=="__main__":
    ingest()
    # add_new_document('app/data/10_learning_and_development.txt')
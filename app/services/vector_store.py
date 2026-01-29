from chromadb import Client
from chromadb.config import Settings
from typing import List, Dict


VECTOR_DB_PATH = 'vector_db'
COLLECTION_NAME = 'pdf_chunks'


client = Client(Settings(
    persist_directory=VECTOR_DB_PATH,
    anonymized_telemetry=False
))

collection = client.get_or_create_collection(name=COLLECTION_NAME)



def store_embeddings(embedded_chunks : List[Dict]):
    ids = []
    documents = []
    metadatas = []
    embeddings = []
    
    for i , chunk in enumerate(embedded_chunks):
        ids.append(f'chunk_{i}')
        documents.append(chunk['content'])
        metadatas.append(chunk['metadata'])
        embeddings.append(chunk['vector'])
    
    collection.add(
        ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings
    )
    
    print(f"✅ Stored {len(embedded_chunks)} chunks")
    
    
def search_similar(query_vector, k=3):
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=k
    )
    
    
    matches = []
    
    for i in range(len(results['ids'][0])):
        match = {
            'id': results['ids'][0][i],
            'content': results['documents'][0][i],
            'metadata': results['metadatas'][0][i],
            'distance': results['distances'][0][i]
        }
        matches.append(match)
    
    return matches



 
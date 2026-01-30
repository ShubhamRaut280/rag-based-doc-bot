import os
from typing import Dict, List, Any
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")


if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    ) 

index = pc.Index(INDEX_NAME)








def store_embeddings(embedded_chunks : List[Any]):
    vectors = []
    
    for i, chunk in enumerate(embedded_chunks):
        vectors.append(
            (
                f'chunk_{i}',
                chunk['vector'],
                {
                    "text" : chunk['content'],
                    **chunk['metadata']
                }
        )
        )
    
    index.upsert(vectors=vectors)
    
def search_similar(query_vector, k=3):
    results = index.query(
        vector=query_vector,     # REQUIRED
        top_k=k,
        include_metadata=True
    )
    return results["matches"]




 
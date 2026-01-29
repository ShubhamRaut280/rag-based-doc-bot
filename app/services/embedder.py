from sentence_transformers import SentenceTransformer
from typing import List, Dict

embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(chunks:List[Dict]) -> List[Dict]:
    texts = [chunk['content'] for chunk in chunks]
    
    embeddings = embed_model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    )
    
    embedded_chunks = []
    
    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append({
            "content": chunk['content'],
            "metadata": chunk['metadata'],
            "vector": embedding.tolist()
        })
    return embedded_chunks


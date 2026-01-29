from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict
 

def chunk_pages(pages : List[Dict]) -> List[Dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    chunks = []
    
    for page in pages:
        texts = splitter.split_text(page['text'])
        
        for idx, text in enumerate(texts):
            chunks.append({
                "content" : text,
                "metadata" : {
                    "source" : page['source'],
                    "page" : page['page'],
                    "chunk_index" : idx
                }
            })
            
    return chunks



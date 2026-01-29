from langchain.chat_models import init_chat_model
from embedder import generate_embeddings
from vector_store import search_similar
from dotenv import load_dotenv
import os

load_dotenv()

model = init_chat_model("google_genai:gemini-2.5-flash-lite")

def answer_question(question: str) -> dict:
    
    query_vector = generate_embeddings([{"content" : question ,"metadata":{}}])[0]['vector']
    search_res = search_similar(query_vector, 3)
    
    context = "\n\n".join([res['content'] for res in search_res])
    
    prompt = f'''Answer the following question using this provided documents context only 
     context : {context}, question is : {question}'''
     
    result = model.invoke(prompt)

    source = [res['metadata'] for res in search_res]
    
    return {
        "answer": result.content,
        "sources": source
    }



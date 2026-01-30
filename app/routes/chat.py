from fastapi import APIRouter, HTTPException
from app.services.qa import answer_question

chatRouter = APIRouter(prefix='/chat', tags=['Chat'])



@chatRouter.post("/")
async def chat(question: str):
    try:
        return answer_question(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 

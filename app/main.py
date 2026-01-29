from fastapi import FastAPI

from app.routes.upload import uploadRouter
from app.routes.chat import chatRouter



app = FastAPI()

app.include_router(uploadRouter)

app.include_router(chatRouter)
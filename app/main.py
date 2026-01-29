from fastapi import FastAPI

from app.routes.upload import uploadRouter



app = FastAPI()

app.include_router(uploadRouter)
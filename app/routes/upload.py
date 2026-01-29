from fastapi import APIRouter, UploadFile, File, HTTPException
import os 
from app.core.config import UPLOAD_DIR
import uuid

uploadRouter = APIRouter(prefix='/upload', tags=['Upload images'])

allowedFileTypes = ['application/pdf']


@uploadRouter.post("/")
async def  uploadFiles(files : list[UploadFile] = File(...)):
    saved_files = []
    
    print(UPLOAD_DIR)

    for file in files : 
        if(file.content_type not in allowedFileTypes): 
            raise HTTPException(
                status_code=400, 
                detail=f'Only following types are allowed : {allowedFileTypes}'
            )

        file_id = f'${uuid.uuid4()}-${file.filename}'
        file_path = UPLOAD_DIR + '/' + file_id
        with open(file_path, 'wb') as f :
            f.write(await file.read())
        
        saved_files.append(file_path)


    
    return {
        "msg" : "Files are uploaded",
        "saved_files" : saved_files
    }


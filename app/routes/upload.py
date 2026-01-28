from fastapi import APIRouter, UploadFile, File, HTTPException
import os 
from app.core.config import UPLOAD_DIR
import uuid

router = APIRouter(prefix='/uplaod', tags=['Upload images'])

allowedFileTypes = ['application/pdf']


@router.post("/")
async def  uplaodImages(files : list[UploadFile] = File(...)):
    saved_files = []

    for file in files : 
        if(file.content_type not in allowedFileTypes): 
            raise HTTPException(
                status_code=400, 
                detail=f'Only following types are allowed ${[type[11 :] for type in allowedFileTypes]}'
            )

        file_id = f'${uuid.uuid4()}-${file.filename}'
        file_path = UPLOAD_DIR + file_id
        with open(file_path, 'w') as f :
            f.write(await file.read())
        
        saved_files.append(file_path)


    
    return {
        "msg" : "Files are uploaded",
        "saved_files" : saved_files
    }


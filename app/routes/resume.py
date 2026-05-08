import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.models import ParseResponse
from app.services.parser import extract_text, extract_rules_based_data
from app.services.llm_service import extract_resume_data
from app.storage.db import save_resume, get_resume
from app.utils.logger import logger

router = APIRouter(prefix="/api", tags=["Resume"])
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=ParseResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.pdf', '.docx','.doc')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")

    doc_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{file.filename}")

    try:
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Parse text
        raw_text = extract_text(file_path, file.filename)
        if len(raw_text.strip()) < 50:
            raise ValueError("Extracted text is too short. File might be scanned/image-based.")
            
        # Extract hybrid data
        regex_data = extract_rules_based_data(raw_text)
        structured_data = extract_resume_data(raw_text, regex_data)
        
        # Save to DB
        save_resume(doc_id, structured_data)
        
        return ParseResponse(document_id=doc_id, data=structured_data)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Internal Error processing {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred during processing.")

@router.get("/resume/{document_id}", response_model=ParseResponse)
async def fetch_resume(document_id: str):
    data = get_resume(document_id)
    if not data:
        raise HTTPException(status_code=404, detail="Resume not found")
    return ParseResponse(document_id=document_id, data=data)
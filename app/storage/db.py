import os
import json
from app.models import ResumeData
from app.utils.logger import logger

PARSED_DIR = "data/parsed"
os.makedirs(PARSED_DIR, exist_ok=True)

def save_resume(doc_id: str, data: ResumeData):
    filepath = os.path.join(PARSED_DIR, f"{doc_id}.json")
    with open(filepath, "w") as f:
        f.write(data.model_dump_json(indent=4))
    logger.info(f"Saved parsed data for {doc_id}")

def get_resume(doc_id: str) -> ResumeData:
    filepath = os.path.join(PARSED_DIR, f"{doc_id}.json")
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as f:
        return ResumeData(**json.load(f))
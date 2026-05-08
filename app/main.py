from fastapi import FastAPI
from app.routes.resume import router
from app.utils.logger import logger

app = FastAPI(title="AI Resume Parser API", version="1.0.0")

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting AI Resume Parser API...")
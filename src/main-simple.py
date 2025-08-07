"""
Simple version without data processing dependencies
"""
from fastapi import FastAPI
import uvicorn
from loguru import logger

app = FastAPI(
    title="Environmental Monitor API",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Environmental Monitor is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    logger.info("🚀 Starting Environmental Monitor")
    uvicorn.run(
        "main-simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
"""
FastAPI Backend for Policy Chatbot
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import shutil
import os
from pathlib import Path

from chatbot import PolicyChatbot
from vector_store import VectorStore
from ingest import ingest_documents
from config import UPLOAD_DIR

app = FastAPI(title="Policy Chatbot API")

# Serve frontend static files
frontend_dist = Path(__file__).parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")
    
    @app.get("/")
    async def serve_frontend():
        return FileResponse(str(frontend_dist / "index.html"))
else:
    @app.get("/")
    async def root():
        return {"message": "Policy Chatbot API is running"}

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Chatbot
chatbot = PolicyChatbot()
vector_store = VectorStore()

class QueryRequest(BaseModel):
    question: str

class Source(BaseModel):
    document: str
    page: Optional[int]
    section: str
    similarity: float

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    confidence: str
    context_chunks: int

@app.post("/api/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    try:
        import time
        start_time = time.time()
        response = chatbot.query(request.question)
        response['response_time'] = round(time.time() - start_time, 2)
        response['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    return vector_store.get_collection_stats()

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Save file to uploads directory
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Trigger ingestion for this file
        ingest_documents(pdf_paths=[str(file_path)])
        
        return {"message": f"Successfully uploaded and processed {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reingest")
async def reingest_all():
    try:
        ingest_documents(clear_existing=True)
        return {"message": "Database cleared and all documents re-ingested"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

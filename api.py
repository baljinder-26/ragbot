print("🚀 STARTING BACKEND...")

import os
import sys
from dotenv import load_dotenv

# Ensure the root and backend folders are in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

try:
    from backend.engine import chat
    from backend.pdf_utils import (
        save_uploaded_pdf,
        create_faiss_from_pdf,
        delete_pdf,
        delete_all_pdfs,
        clear_database,
        list_pdfs
    )
except Exception as e:
    print(f"❌ CRITICAL IMPORT ERROR: {e}")
    import traceback
    traceback.print_exc()
    raise e

# ------------------------
# Create App
# ------------------------

app = FastAPI()

# ------------------------
# Enable CORS
# ------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Request Models
# ------------------------

class ChatRequest(BaseModel):
    message: str
    user_id: str

class DeletePDFRequest(BaseModel):
    filename: str
    user_id: str

# ------------------------
# Root
# ------------------------

@app.get("/")
def home():
    return {
        "message": "RAG Chatbot API Running 🚀"
    }

# ------------------------
# Endpoints (Using backend functions)
# ------------------------

@app.post("/chat")
async def chat_api(request: ChatRequest):
    response = chat(request.message, request.user_id)
    return {"response": response}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), user_id: str = Form(...)):
    pdf_path = save_uploaded_pdf(file)
    create_faiss_from_pdf(pdf_path, user_id)
    return {"message": "PDF uploaded successfully"}

@app.post("/delete-pdf")
async def delete_pdf_api(request: DeletePDFRequest):
    success = delete_pdf(request.filename, request.user_id)
    if success:
        return {"message": "PDF deleted successfully 🗑"}
    return {"error": "File not found"}

@app.post("/delete-all-pdfs")
async def delete_all_api(user_id: str = Form(...)):
    success = delete_all_pdfs(user_id)
    if success:
        return {"message": "All PDFs deleted successfully 🧹"}
    return {"error": "Delete all PDFs failed"}

@app.post("/clear-database")
async def clear_db(user_id: str = Form(...)):
    success = clear_database(user_id)
    if success:
        return {"message": "Database cleared successfully 🧹"}
    return {"error": "Database clear failed"}

@app.get("/list-pdfs")
async def list_files(user_id: str):
    files = list_pdfs(user_id)
    return {"files": files}
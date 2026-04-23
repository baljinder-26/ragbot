print("[DEBUG] api.py loaded successfully")

import os
import sys
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add backend folder to path just in case
sysPath = os.path.dirname(os.path.abspath(__file__))
if sysPath not in sys.path:
    sys.path.append(sysPath)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    user_id: str

class DeletePDFRequest(BaseModel):
    filename: str
    user_id: str

@app.get("/")
def home():
    print("[DEBUG] Root endpoint hit")
    return {"status": "online", "message": "Nexus RAG API is live"}

@app.post("/chat")
async def chat_api(request: ChatRequest):
    # LAZY IMPORT: Only loads AI logic when the first message arrives
    from backend.engine import chat
    response = chat(request.message, request.user_id)
    return {"response": response}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), user_id: str = Form(...)):
    from backend.pdf_utils import save_uploaded_pdf, create_faiss_from_pdf
    pdf_path = save_uploaded_pdf(file)
    create_faiss_from_pdf(pdf_path, user_id)
    return {"message": "PDF uploaded successfully"}

@app.get("/list-pdfs")
async def list_files(user_id: str):
    from backend.pdf_utils import list_pdfs
    files = list_pdfs(user_id)
    return {"files": files}

@app.post("/delete-pdf")
async def delete_pdf_api(request: DeletePDFRequest):
    from backend.pdf_utils import delete_pdf
    success = delete_pdf(request.filename, request.user_id)
    return {"message": "Success" if success else "Failed"}

@app.post("/delete-all-pdfs")
async def delete_all_api(user_id: str = Form(...)):
    from backend.pdf_utils import delete_all_pdfs
    success = delete_all_pdfs(user_id)
    return {"message": "Success" if success else "Failed"}

@app.post("/clear-database")
async def clear_db(user_id: str = Form(...)):
    from backend.pdf_utils import clear_database
    success = clear_database(user_id)
    return {"message": "Success" if success else "Failed"}





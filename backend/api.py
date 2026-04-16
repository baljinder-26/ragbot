
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import Form
from dotenv import load_dotenv
import os

load_dotenv()
# Chat Logic
from engine import chat

# PDF Utilities
from pdf_utils import (
    save_uploaded_pdf,
    create_faiss_from_pdf,
    delete_pdf,
    delete_all_pdfs,
    clear_database,
    list_pdfs
)


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
# Chat Endpoint
# ------------------------

# @app.post("/chat")
# async def chat_api(request: ChatRequest):

#     response = chat(
#         request.message
#     )

#     return {
#         "response": response
#     }
@app.post("/chat")
async def chat_api(request: ChatRequest):

    response = chat(

        request.message,
        request.user_id   # ⭐ VERY IMPORTANT

    )

    return {
        "response": response
    }# ------------------------
# Upload PDF
# ------------------------

# @app.post("/upload-pdf")
# async def upload_pdf(
#     file: UploadFile = File(...)
# ):

#     pdf_path = save_uploaded_pdf(
#         file
#     )

#     create_faiss_from_pdf(
#         pdf_path
#     )

#     return {
#         "message": "PDF uploaded and indexed successfully ✅"
#     }
@app.post("/upload-pdf")
async def upload_pdf(

    file: UploadFile = File(...),
    user_id: str = Form(...)

):

    pdf_path = save_uploaded_pdf(file)

    create_faiss_from_pdf(
        pdf_path,
        user_id     # ⭐ PASS user_id
    )

    return {
        "message": "PDF uploaded successfully"
    }

# ------------------------
# Delete Single PDF
# ------------------------

# @app.post("/delete-pdf")
# async def delete_pdf_api(
#     request: DeletePDFRequest
# ):

#     success = delete_pdf(
#         request.filename
#     )

#     if success:

#         return {
#             "message": "PDF deleted successfully 🗑"
#         }

#     return {
#         "error": "File not found"
#     }
@app.post("/delete-pdf")
async def delete_pdf_api(
    request: DeletePDFRequest
):

    success = delete_pdf(

        request.filename,
        request.user_id   # ⭐ ADD

    )

    if success:

        return {
            "message": "PDF deleted successfully 🗑"
        }

    return {
        "error": "File not found"
    }


# ------------------------
# Delete All PDFs
# ------------------------
# @app.post("/delete-all-pdfs")
# async def delete_all_api():

#     success = delete_all_pdfs()

#     if success:

#         return {
#             "message": "All PDFs deleted successfully 🧹"
#         }

#     return {
#         "error": "Delete all PDFs failed"
#     }
@app.post("/delete-all-pdfs")
async def delete_all_api(

    user_id: str = Form(...)

):

    success = delete_all_pdfs(

        user_id   # ⭐ ADD

    )

    if success:

        return {
            "message": "All PDFs deleted successfully 🧹"
        }

    return {
        "error": "Delete all PDFs failed"
    }

# ------------------------
# Clear Entire Database
# ------------------------


# @app.post("/clear-database")
# async def clear_db():

#     success = clear_database()

#     if success:

#         return {
#             "message": "Database cleared successfully 🧹"
#         }

#     return {
#         "error": "Database clear failed"
#     }
@app.post("/clear-database")
async def clear_db(

    user_id: str = Form(...)

):

    success = clear_database(

        user_id   # ⭐ ADD

    )

    if success:

        return {
            "message": "Database cleared successfully 🧹"
        }

    return {
        "error": "Database clear failed"
    }

# ------------------------
# List Uploaded PDFs
# ------------------------

# @app.get("/list-pdfs")
# async def list_files():

#     files = list_pdfs()

#     return {
#         "files": files
#     }
@app.get("/list-pdfs")
async def list_files(

    user_id: str

):

    files = list_pdfs(

        user_id   # ⭐ ADD

    )

    return {
        "files": files
    }
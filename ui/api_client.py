# import requests

# BASE_URL = "http://127.0.0.1:8000"


# # ------------------------
# # Chat API
# # ------------------------

# def send_message(message):

#     url = f"{BASE_URL}/chat"

#     response = requests.post(
#         url,
#         json={"message": message}
#     )

#     return response.json()["response"]


# # ------------------------
# # Upload PDF
# # ------------------------

# def upload_pdf(file):

#     url = f"{BASE_URL}/upload-pdf"

#     files = {
#         "file": (
#             file.name,
#             file,
#             "application/pdf"
#         )
#     }

#     response = requests.post(
#         url,
#         files=files
#     )

#     return response.json()


# # ------------------------
# # List PDFs
# # ------------------------

# def list_pdfs():

#     url = f"{BASE_URL}/list-pdfs"

#     response = requests.get(url)

#     return response.json()["files"]


# # ------------------------
# # Delete Single PDF
# # ------------------------

# def delete_pdf(filename):

#     url = f"{BASE_URL}/delete-pdf"

#     response = requests.post(
#         url,
#         json={"filename": filename}
#     )

#     return response.json()


# # ------------------------
# # Delete All PDFs
# # ------------------------

# def delete_all_pdfs():

#     url = f"{BASE_URL}/delete-all-pdfs"

#     response = requests.post(url)

#     return response.json()


# # ------------------------
# # Clear Database
# # ------------------------

# def clear_database():

#     url = f"{BASE_URL}/clear-database"

#     response = requests.post(url)

#     return response.json()


import os
import requests
import streamlit as st

# Local: http://127.0.0.1:8000
# Cloud: set BACKEND_URL in Streamlit Cloud Secrets
BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


# ------------------------
# Chat API
# ------------------------
def send_message(message):
    url = f"{BASE_URL}/chat"
    try:
        response = requests.post(
            url,
            json={
                "message": message,
                "user_id": st.session_state.user_id
            },
            timeout=120 # Wait up to 2 mins for backend to wake up and LLM to respond
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        return "⚠️ Backend is either waking up or unreachable. If you're on a free hosting tier, it takes ~50s to wake up from sleep. Please try again in a moment."


# ------------------------
# Upload PDF
# ------------------------
def upload_pdf(file):
    url = f"{BASE_URL}/upload-pdf"
    files = {
        "file": (
            file.name,
            file.getvalue(),
            "application/pdf"
        )
    }
    data = {
        "user_id": st.session_state.user_id
    }
    try:
        response = requests.post(
            url,
            files=files,
            data=data,
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"message": "⚠️ Upload failed: Backend is sleeping or unreachable. Wait 60s and try again."}


# ------------------------
# List PDFs
# ------------------------
def list_pdfs():
    url = f"{BASE_URL}/list-pdfs"
    params = {
        "user_id": st.session_state.user_id
    }
    try:
        # Initial poll should be quick so frontend doesn't hang!
        response = requests.get(
            url,
            params=params,
            timeout=5
        )
        response.raise_for_status()
        return response.json()["files"]
    except Exception:
        # Fails silently and returns empty list so UI can load
        return []

# ------------------------
# Delete Single PDF
# ------------------------
def delete_pdf(filename):
    url = f"{BASE_URL}/delete-pdf"
    try:
        response = requests.post(
            url,
            json={
                "filename": filename,
                "user_id": st.session_state.user_id
            },
            timeout=60
        )
        return response.json()
    except Exception:
        return {"message": "Failed"}

# ------------------------
# Delete All PDFs
# ------------------------
def delete_all_pdfs():
    url = f"{BASE_URL}/delete-all-pdfs"
    data = {
        "user_id": st.session_state.user_id
    }
    try:
        response = requests.post(
            url,
            data=data,
            timeout=60
        )
        return response.json()
    except Exception:
        return {"message": "Failed"}


# ------------------------
# Clear Database
# ------------------------
def clear_database():
    url = f"{BASE_URL}/clear-database"
    data = {
        "user_id": st.session_state.user_id
    }
    try:
        response = requests.post(
            url,
            data=data,
            timeout=60
        )
        return response.json()
    except Exception:
        return {"message": "Failed"}
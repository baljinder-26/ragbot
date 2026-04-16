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

    response = requests.post(

        url,

        json={
            "message": message,
            "user_id": st.session_state.user_id   # ⭐ ADD THIS
        }

    )

    return response.json()["response"]


# ------------------------
# Upload PDF (FIXED)
# ------------------------

# def upload_pdf(file):

#     url = f"{BASE_URL}/upload-pdf"

#     files = {
#         "file": (
#             file.name,
#             file.getvalue(),   # ✅ FIX HERE
#             "application/pdf"
#         )
#     }

#     response = requests.post(
#         url,
#         files=files
#     )

#     return response.json()
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

        "user_id": st.session_state.user_id   # ⭐ ADD THIS

    }

    response = requests.post(

        url,

        files=files,
        data=data     # ⭐ VERY IMPORTANT

    )

    return response.json()


# ------------------------
# List PDFs
# ------------------------

# def list_pdfs():

#     url = f"{BASE_URL}/list-pdfs"

#     response = requests.get(url)

#     return response.json()["files"]
def list_pdfs():

    url = f"{BASE_URL}/list-pdfs"

    params = {

        "user_id": st.session_state.user_id

    }

    response = requests.get(

        url,
        params=params

    )

    return response.json()["files"]

# ------------------------
# Delete Single PDF
# ------------------------

# def delete_pdf(filename):

#     url = f"{BASE_URL}/delete-pdf"

#     response = requests.post(
#         url,
#         json={"filename": filename},
#         timeout=60
#     )

#     print("DELETE RESPONSE:", response.json())

#     return response.json()
def delete_pdf(filename):

    url = f"{BASE_URL}/delete-pdf"

    response = requests.post(

        url,

        json={

            "filename": filename,
            "user_id": st.session_state.user_id   # ⭐ ADD

        },

        timeout=60

    )

    print("DELETE RESPONSE:", response.json())

    return response.json()

# ------------------------
# Delete All PDFs
# ------------------------

# def delete_all_pdfs():

#     url = f"{BASE_URL}/delete-all-pdfs"

#     response = requests.post(url)

#     return response.json()
def delete_all_pdfs():

    url = f"{BASE_URL}/delete-all-pdfs"

    data = {

        "user_id": st.session_state.user_id

    }

    response = requests.post(

        url,
        data=data

    )

    return response.json()


# ------------------------
# Clear Database
# ------------------------

# def clear_database():

#     url = f"{BASE_URL}/clear-database"

#     response = requests.post(url)

#     return response.json()
def clear_database():

    url = f"{BASE_URL}/clear-database"

    data = {

        "user_id": st.session_state.user_id

    }

    response = requests.post(

        url,
        data=data

    )

    return response.json()
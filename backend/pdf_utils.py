
# import os
# import shutil

# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from qdrant_client.models import PayloadSchemaType
# from langchain_qdrant import QdrantVectorStore
# from qdrant_client import QdrantClient
# from dotenv import load_dotenv
# from langchain_community.embeddings import HuggingFaceEmbeddings

# from qdrant_client.models import Filter, FieldCondition, MatchValue
# # ------------------------
# # Base Paths
# # ------------------------

# load_dotenv()

# QDRANT_URL = os.getenv("QDRANT_URL")
# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# client = QdrantClient(
#     url=QDRANT_URL,
#     api_key=QDRANT_API_KEY
# )

# COLLECTION_NAME = "pdf_docs"
# # ------

# BASE_DIR = os.path.dirname(
#     os.path.dirname(os.path.abspath(__file__))
# )

# PDF_FOLDER = os.path.join(
#     BASE_DIR,
#     "data",
#     "pdfs"
# )

# FAISS_PATH = os.path.join(
#     BASE_DIR,
#     "data",
#     "faiss_db"
# )


# # Ensure folders exist
# os.makedirs(PDF_FOLDER, exist_ok=True)
# os.makedirs(FAISS_PATH, exist_ok=True)


# # ------------------------
# # Embeddings Model
# # ------------------------

# embeddings = HuggingFaceEmbeddings(
#     # model_name="BAAI/bge-small-en-v1.5"
#       model_name="sentence-transformers/all-MiniLM-L6-v2"
# )#"BAAI/bge-base-en-v1.5"


# def create_user_index():

#     try:

#         client.create_payload_index(

#             collection_name=COLLECTION_NAME,

#             field_name="user_id",

#             field_schema=PayloadSchemaType.KEYWORD

#         )

#         print("✅ user_id index created")

#     except Exception as e:

#         print("Index exists or error:", e)

# # ------------------------
# # Save Uploaded PDF
# # ------------------------

# def save_uploaded_pdf(file):

#     file_path = os.path.join(
#         PDF_FOLDER,
#         file.filename
#     )

#     with open(file_path, "wb") as f:

#         f.write(file.file.read())

#     return file_path




# # ------------------------
# # Create FAISS From Upload
# # ------------------------

# # def create_faiss_from_pdf(pdf_path):

# #     rebuild_faiss()

# #     return True
# # def create_faiss_from_pdf(pdf_path):

# #     loader = PyPDFLoader(pdf_path)

# #     documents = loader.load()

# #     splitter = RecursiveCharacterTextSplitter(
# #         chunk_size=1200,
# #         chunk_overlap=400
# #     )

   
# #     chunks = splitter.split_documents(documents)

# # # ✅ Add filename metadata
# #     filename = os.path.basename(pdf_path)

# #     for chunk in chunks:
# #         chunk.metadata["source"] = filename

# #     vectorstore = QdrantVectorStore.from_documents(
# #         documents=chunks,
# #         embedding=embeddings,
# #         url=QDRANT_URL,
# #         api_key=QDRANT_API_KEY,
# #         collection_name=COLLECTION_NAME
# #     )

# #     print("✅ PDF stored in Qdrant")

# #     return True

# def create_faiss_from_pdf(
#     pdf_path,
#     user_id
# ):

#     loader = PyPDFLoader(pdf_path)

#     documents = loader.load()

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1200,
#         chunk_overlap=400
#     )

#     chunks = splitter.split_documents(documents)

#     filename = os.path.basename(pdf_path)

#     for chunk in chunks:

#         chunk.metadata["source"] = filename
#         chunk.metadata["user_id"] = user_id

#     # STEP 1 — Create collection (if not exists)
#     vectorstore = QdrantVectorStore.from_documents(

#         documents=chunks,

#         embedding=embeddings,

#         url=QDRANT_URL,
#         api_key=QDRANT_API_KEY,

#         collection_name=COLLECTION_NAME

#     )

#     # STEP 2 — Create user_id index AFTER collection exists
#     try:

#         client.create_payload_index(

#             collection_name=COLLECTION_NAME,

#             field_name="user_id",

#             field_schema=PayloadSchemaType.KEYWORD

#         )

#         print("✅ user_id index created")

#     except Exception as e:

#         print("Index exists or error:", e)

#     print("✅ PDF stored in Qdrant")

#     return True
# # ------------------------
# # Delete Single PDF
# # ------------------------

# # def delete_pdf(filename):

# #     file_path = os.path.join(
# #         PDF_FOLDER,
# #         filename
# #     )

# #     if not os.path.exists(file_path):
# #         return False

# #     # Delete local file
# #     os.remove(file_path)

# #     try:

# #         # Delete vectors from Qdrant
# #         client.delete(
# #             collection_name=COLLECTION_NAME,
# #             points_selector=Filter(
# #                 must=[
# #                     FieldCondition(
# #                         key="source",
# #                         match=MatchValue(value=filename)
# #                     )
# #                 ]
# #             )
# #         )

# #         print(f"🗑 Deleted {filename} from Qdrant")

# #     except Exception as e:

# #         print("Qdrant delete error:", e)

# #     return True

# def delete_pdf(
#     filename,
#     user_id
# ):

#     file_path = os.path.join(
#         PDF_FOLDER,
#         filename
#     )

#     if not os.path.exists(file_path):
#         return False

#     os.remove(file_path)

#     try:

#         client.delete(

#             collection_name=COLLECTION_NAME,

#             points_selector=Filter(

#                 must=[

#                     FieldCondition(
#                         key="source",
#                         match=MatchValue(value=filename)
#                     ),

#                     FieldCondition(
#                         key="user_id",
#                         match=MatchValue(value=user_id)
#                     )

#                 ]

#             )

#         )

#         print(f"🗑 Deleted {filename} from Qdrant")

#     except Exception as e:

#         print("Qdrant delete error:", e)

#     return True

# # ------------------------
# # Delete All PDFs
# # ------------------------

# # def delete_all_pdfs():

# #     try:

# #         # Delete all PDFs locally
# #         if os.path.exists(PDF_FOLDER):

# #             shutil.rmtree(PDF_FOLDER)

# #         # Recreate folder
# #         os.makedirs(PDF_FOLDER, exist_ok=True)

# #         print("🧹 All local PDFs deleted")

# #         return True

# #     except Exception as e:

# #         print("Delete all PDFs error:", e)

# #         return False
# def delete_all_pdfs(user_id):

#     try:

#         client.delete(

#             collection_name=COLLECTION_NAME,

#             points_selector=Filter(

#                 must=[

#                     FieldCondition(
#                         key="user_id",
#                         match=MatchValue(value=user_id)
#                     )

#                 ]

#             )

#         )

#         print("🧹 User PDFs deleted")

#         return True

#     except Exception as e:

#         print("Delete all PDFs error:", e)

#         return False


# # ------------------------
# # Clear FAISS Only
# # ------------------------



# # ------------------------
# # Clear Entire Database
# # ------------------------

# # def clear_database():

# #     try:

# #         # Delete local PDFs
# #         if os.path.exists(PDF_FOLDER):

# #             shutil.rmtree(PDF_FOLDER)

# #         os.makedirs(PDF_FOLDER, exist_ok=True)

# #         # Delete Qdrant collection
# #         try:

# #             client.delete_collection(
# #                 collection_name=COLLECTION_NAME
# #             )

# #             print("🧹 Qdrant collection deleted")

# #         except Exception as e:

# #             print("Collection delete error:", e)

# #         return True

# #     except Exception as e:

# #         print("Clear database error:", e)

# #         return False

# def clear_database(user_id):

#     try:

#         client.delete(

#             collection_name=COLLECTION_NAME,

#             points_selector=Filter(

#                 must=[

#                     FieldCondition(
#                         key="user_id",
#                         match=MatchValue(value=user_id)
#                     )

#                 ]

#             )

#         )

#         print("🧹 User database cleared")

#         return True

#     except Exception as e:

#         print("Clear database error:", e)

#         return False
# # ------------------------
# # List Uploaded PDFs
# # ------------------------

# # def list_pdfs():

# #     files = []

# #     if os.path.exists(PDF_FOLDER):

# #         for file in os.listdir(PDF_FOLDER):

# #             if file.endswith(".pdf"):

# #                 files.append(file)

# #     return files

# def list_pdfs(user_id):

#     files = set()

#     try:

#         scroll_result = client.scroll(

#             collection_name=COLLECTION_NAME,

#             scroll_filter=Filter(

#                 must=[

#                     FieldCondition(
#                         key="user_id",
#                         match=MatchValue(value=user_id)
#                     )

#                 ]

#             ),

#             limit=100

#         )

#         points = scroll_result[0]

#         for point in points:

#             source = point.payload.get("source")

#             if source:

#                 files.add(source)

#     except Exception as e:

#         print("List PDFs error:", e)

#     return list(files)



import os
import shutil

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

from qdrant_client import QdrantClient, models


# ------------------------
# ENV SETUP
# ------------------------

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = "pdf_docs"


# ------------------------
# Qdrant Client
# ------------------------

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)


# ------------------------
# Paths
# ------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

PDF_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "pdfs"
)

os.makedirs(PDF_FOLDER, exist_ok=True)


# ------------------------
# Embeddings
# ------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ------------------------
# Ensure Collection Exists
# ------------------------

def ensure_collection():

    try:

        if not client.collection_exists(COLLECTION_NAME):

            client.create_collection(

                collection_name=COLLECTION_NAME,

                vectors_config=models.VectorParams(
                    size=384,
                    distance=models.Distance.COSINE,
                )

            )

            print("✅ Collection created")

        # Create metadata.user_id index (LangChain nests metadata under 'metadata.*')
        client.create_payload_index(

            collection_name=COLLECTION_NAME,

            field_name="metadata.user_id",

            field_schema=models.PayloadSchemaType.KEYWORD

        )

        print("✅ user_id index ready")

    except Exception as e:

        print("Collection/index error:", e)


# ------------------------
# Save Uploaded PDF
# ------------------------

def save_uploaded_pdf(file):

    file_path = os.path.join(
        PDF_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as f:

        f.write(file.file.read())

    return file_path


# ------------------------
# Upload PDF → Store in Qdrant
# ------------------------

def create_faiss_from_pdf(
    pdf_path,
    user_id
):

    ensure_collection()

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=400
    )

    chunks = splitter.split_documents(documents)

    filename = os.path.basename(pdf_path)

    # Add metadata
    for chunk in chunks:

        chunk.metadata["source"] = filename
        chunk.metadata["user_id"] = user_id

    # Store vectors
    QdrantVectorStore.from_documents(

        documents=chunks,

        embedding=embeddings,

        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,

        collection_name=COLLECTION_NAME

    )

    print("✅ PDF stored in Qdrant")

    return True


# ------------------------
# List PDFs
# ------------------------

def list_pdfs(user_id):

    files = set()

    try:

        scroll_result = client.scroll(

            collection_name=COLLECTION_NAME,

            # LangChain stores metadata under nested 'metadata' key
            scroll_filter=models.Filter(

                must=[

                    models.FieldCondition(
                        key="metadata.user_id",
                        match=models.MatchValue(
                            value=user_id
                        )
                    )

                ]

            ),

            limit=100,

            with_payload=True

        )

        points = scroll_result[0]

        for point in points:

            # LangChain nests metadata inside payload["metadata"]
            metadata = point.payload.get("metadata", {})
            source = metadata.get("source")

            if source:

                files.add(source)

        print("📄 Files found:", files)

    except Exception as e:

        print("List PDFs error:", e)

    return list(files)


# ------------------------
# Delete Single PDF
# ------------------------

def delete_pdf(
    filename,
    user_id
):

    file_path = os.path.join(
        PDF_FOLDER,
        filename
    )

    if os.path.exists(file_path):

        os.remove(file_path)

    try:

        client.delete(

            collection_name=COLLECTION_NAME,

            points_selector=models.FilterSelector(

                filter=models.Filter(

                    must=[

                        # LangChain stores metadata under 'metadata.*'
                        models.FieldCondition(
                            key="metadata.source",
                            match=models.MatchValue(
                                value=filename
                            )
                        ),

                        models.FieldCondition(
                            key="metadata.user_id",
                            match=models.MatchValue(
                                value=user_id
                            )
                        )

                    ]

                )

            )

        )

        print(f"🗑 Deleted {filename}")

        return True

    except Exception as e:

        print("Delete error:", e)

        return False


# ------------------------
# Delete All PDFs (User)
# ------------------------

def delete_all_pdfs(user_id):

    try:

        client.delete(

            collection_name=COLLECTION_NAME,

            points_selector=models.FilterSelector(

                filter=models.Filter(

                    must=[

                        # LangChain stores metadata under 'metadata.*'
                        models.FieldCondition(
                            key="metadata.user_id",
                            match=models.MatchValue(
                                value=user_id
                            )
                        )

                    ]

                )

            )

        )

        print("🧹 User PDFs deleted")

        return True

    except Exception as e:

        print("Delete all error:", e)

        return False


# ------------------------
# Clear Database (User)
# ------------------------

def clear_database(user_id):

    try:

        client.delete(

            collection_name=COLLECTION_NAME,

            points_selector=models.FilterSelector(

                filter=models.Filter(

                    must=[

                        # LangChain stores metadata under 'metadata.*'
                        models.FieldCondition(
                            key="metadata.user_id",
                            match=models.MatchValue(
                                value=user_id
                            )
                        )

                    ]

                )

            )

        )

        print("🧹 User database cleared")

        return True

    except Exception as e:

        print("Clear database error:", e)

        return False
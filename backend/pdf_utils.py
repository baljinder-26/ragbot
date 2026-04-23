



import os
import shutil

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode

from qdrant_client import QdrantClient, models


# ------------------------
# ENV SETUP
# ------------------------

load_dotenv()


HF_TOKEN = os.getenv("HF_TOKEN")


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

# Lazy-loaded — only initialized on first use to save startup memory
# _embeddings = None

# def get_embeddings():
#     global _embeddings
#     if _embeddings is None:
#         _embeddings = HuggingFaceEndpointEmbeddings(
#             api_key=os.getenv("HF_TOKEN"),
#             model_name="sentence-transformers/all-MiniLM-L6-v2"
#         )
#     return _embeddings


_embeddings = None

def get_embeddings():
    global _embeddings

    if _embeddings is None:
        _embeddings = HuggingFaceEndpointEmbeddings(
            model="sentence-transformers/all-MiniLM-L6-v2",
            huggingfacehub_api_token=os.getenv("HF_TOKEN")
        )

    return _embeddings

_sparse_embeddings = None

def get_sparse_embeddings():
    global _sparse_embeddings
    if _sparse_embeddings is None:
        _sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")
    return _sparse_embeddings


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
                ),
                sparse_vectors_config={
                    "langchain-sparse": models.SparseVectorParams()
                }

            )

            print("SUCCESS: Collection created")

        # Create metadata.user_id index (LangChain nests metadata under 'metadata.*')
        client.create_payload_index(

            collection_name=COLLECTION_NAME,

            field_name="metadata.user_id",

            field_schema=models.PayloadSchemaType.KEYWORD

        )

        print("SUCCESS: user_id index ready")

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
        
        chunk.page_content = f"Document: {filename}\n\n" + chunk.page_content

    # Store vectors
    QdrantVectorStore.from_documents(

        documents=chunks,

        embedding=get_embeddings(),
        sparse_embedding=get_sparse_embeddings(),
        retrieval_mode=RetrievalMode.HYBRID,

        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,

        collection_name=COLLECTION_NAME

    )

    print("SUCCESS: PDF stored in Qdrant")

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

        print("FILES: Files found:", files)

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

        print(f"DELETED: {filename}")

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

        print("CLEANUP: User PDFs deleted")

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

        print("CLEANUP: User database cleared")

        return True

    except Exception as e:

        print("Clear database error:", e)

        return False


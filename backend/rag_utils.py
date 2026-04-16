# import os


# from langchain_qdrant import QdrantVectorStore
# from qdrant_client import QdrantClient
# from dotenv import load_dotenv
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores.utils import DistanceStrategy


# load_dotenv()

# QDRANT_URL = os.getenv("QDRANT_URL")
# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# client = QdrantClient(
#     url=QDRANT_URL,
#     api_key=QDRANT_API_KEY
# )

# COLLECTION_NAME = "pdf_docs"

# # ------------------------
# # Base Paths
# # ------------------------

# BASE_DIR = os.path.dirname(
#     os.path.dirname(os.path.abspath(__file__))
# )

# FAISS_PATH = os.path.join(
#     BASE_DIR,
#     "data",
#     "faiss_db"
# )


# # ------------------------
# # Embeddings Model (Cosine Ready)
# # ------------------------

# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2",
#     encode_kwargs={
#         "normalize_embeddings": True  # ⭐ Important
#     }
# )


# # ------------------------
# # Check if FAISS Exists
# # ------------------------

# def faiss_exists():

#     index_file = os.path.join(
#         FAISS_PATH,
#         "index.faiss"
#     )

#     return os.path.exists(index_file)


# # ------------------------
# # Load Retriever (Improved)
# # ------------------------

# def load_retriever():

#     vectorstore = QdrantVectorStore(
#         client=client,
#         collection_name=COLLECTION_NAME,
#         embedding=embeddings
#     )

#     retriever = vectorstore.as_retriever(
#         search_type="mmr",
#         search_kwargs={
#             "k": 5,
#             "fetch_k": 20
#         }
#     )

#     print("✅ Retriever loaded from Qdrant")

#     return retriever

# # ------------------------
# # Keyword Boost (Fix Figure Numbers)
# # ------------------------

# import re

# def keyword_boost_filter(query, docs):

#     boosted_docs = []

#     # Extract figure numbers like 21.4
#     figure_numbers = re.findall(
#         r"\d+\.\d+",
#         query
#     )

#     query_words = query.lower().split()

#     for doc in docs:

#         text = doc.page_content.lower()

#         score = 0

#         # Word match
#         for word in query_words:

#             if word in text:
#                 score += 1

#         # ⭐ Figure number match
#         for num in figure_numbers:

#             if num in text:
#                 score += 10   # BIG BOOST

#         boosted_docs.append((score, doc))

#     boosted_docs.sort(
#         key=lambda x: x[0],
#         reverse=True
#     )

#     return [doc for _, doc in boosted_docs]
# # ------------------------
# # Get Context from Query (Improved)
# # ------------------------
# def keyword_boost_filter(query, docs):

#     boosted_docs = []

#     query_words = query.lower().split()

#     for doc in docs:

#         text = doc.page_content.lower()

#         score = 0

#         for word in query_words:

#             if word in text:
#                 score += 1

#         boosted_docs.append((score, doc))

#     boosted_docs.sort(
#         key=lambda x: x[0],
#         reverse=True
#     )

#     return [doc for _, doc in boosted_docs]


# # ⭐ ADD THIS FUNCTION

# def format_docs(docs):

#     if not docs:
#         return ""

#     return "\n\n".join(
#         doc.page_content
#         for doc in docs
#     )


# # ------------------------
# # Get Context
# # ------------------------

# def get_context(query):

#     retriever = load_retriever()

#     if retriever is None:
#         return ""

#     docs = retriever.invoke(query)

#     docs = keyword_boost_filter(
#         query,
#         docs
#     )

#     context = format_docs(docs)

#     return context

import os
import re

from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings

from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue
)

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

COLLECTION_NAME = "pdf_docs"


# ------------------------
# Embeddings Model
# ------------------------

embeddings = HuggingFaceEmbeddings(

    model_name="sentence-transformers/all-MiniLM-L6-v2",

    encode_kwargs={

        "normalize_embeddings": True

    }

)


# ------------------------
# Load Retriever
# ------------------------

def load_retriever(user_id):

    vectorstore = QdrantVectorStore(

        client=client,

        collection_name=COLLECTION_NAME,

        embedding=embeddings

    )

    retriever = vectorstore.as_retriever(

        search_type="mmr",

        search_kwargs={

            "k": 5,

            "fetch_k": 20,

            # ⭐ USER FILTER — LangChain stores metadata under 'metadata.*'
            "filter": Filter(

                must=[

                    FieldCondition(

                        key="metadata.user_id",

                        match=MatchValue(

                            value=user_id

                        )

                    )

                ]

            )

        }

    )

    print(f"✅ Retriever loaded for user: {user_id}")

    return retriever


# ------------------------
# Keyword Boost Filter
# ------------------------

def keyword_boost_filter(query, docs):

    boosted_docs = []

    # Extract figure numbers like 21.4
    figure_numbers = re.findall(
        r"\d+\.\d+",
        query
    )

    query_words = query.lower().split()

    for doc in docs:

        text = doc.page_content.lower()

        score = 0

        # Word match
        for word in query_words:

            if word in text:
                score += 1

        # Figure number boost
        for num in figure_numbers:

            if num in text:
                score += 10

        boosted_docs.append((score, doc))

    boosted_docs.sort(

        key=lambda x: x[0],

        reverse=True

    )

    return [doc for _, doc in boosted_docs]


# ------------------------
# Format Docs
# ------------------------

def format_docs(docs):

    if not docs:

        return ""

    return "\n\n".join(

        doc.page_content

        for doc in docs

    )


# ------------------------
# Get Context (FINAL)
# ------------------------

def get_context(

    query,
    user_id

):

    retriever = load_retriever(

        user_id

    )

    if retriever is None:

        return ""

    docs = retriever.invoke(

        query

    )

    docs = keyword_boost_filter(

        query,
        docs

    )

    context = format_docs(

        docs

    )

    return context
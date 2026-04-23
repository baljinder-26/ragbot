

import os
import re

from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode
from qdrant_client import QdrantClient
from dotenv import load_dotenv
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue
)

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")


HF_TOKEN = os.getenv("HF_TOKEN")


client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

COLLECTION_NAME = "pdf_docs"


# ------------------------
# Embeddings Model
# ------------------------

# Lazy-loaded — only initialized on first use to save startup memory
_embeddings = None

# _embeddings = None

# def get_embeddings():
#     global _embeddings
#     if _embeddings is None:
#         _embeddings = HuggingFaceEndpointEmbeddings(
#             api_key=os.getenv("HF_TOKEN"),
#             model_name="sentence-transformers/all-MiniLM-L6-v2"
#         )
#     return _embeddings



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
# Load Retriever
# ------------------------

def load_retriever(user_id):

    vectorstore = QdrantVectorStore(

        client=client,

        collection_name=COLLECTION_NAME,

        embedding=get_embeddings(),
        sparse_embedding=get_sparse_embeddings(),
        retrieval_mode=RetrievalMode.HYBRID,

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

    print(f"SUCCESS: Retriever loaded for user: {user_id}")

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



import os

from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate

from huggingface_hub import InferenceClient

# Import RAG helpers
from backend.rag_utils import get_context


# ------------------------
# ENV SETUP
# ------------------------

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")


# ------------------------
# LLM Setup
# ------------------------

client = InferenceClient(

    model="meta-llama/Llama-3.1-8B-Instruct",

    token=HF_TOKEN

)


# ------------------------
# Chat Memory (Multi-user)
# ------------------------

chat_histories = {}


def get_history_text(user_id):

    # Create history if new user

    if user_id not in chat_histories:

        chat_histories[user_id] = []

    return "\n".join(

        chat_histories[user_id][-6:]

    )


# ------------------------
# Prompt Template
# ------------------------

prompt_template = PromptTemplate.from_template(
"""
You are a helpful AI assistant.

Previous Conversation:
{history}

Use the provided context if available.

Context:
{context}

User Question:
{question}

Instructions:
- If context is available → answer using it
- If no context → answer normally
- Keep answers clear
- Use examples if useful

Answer:
"""
)


# ------------------------
# LLM Call Function
# ------------------------

def call_llm(prompt_text):

    response = client.chat.completions.create(

        messages=[

            {

                "role": "user",

                "content": prompt_text

            }

        ],

        max_tokens=512,

        temperature=0.3

    )

    return response.choices[0].message.content


# ------------------------
# MAIN CHAT FUNCTION
# ------------------------

def chat(

    user_input,
    user_id

):

    # ------------------------
    # Get user history
    # ------------------------

    history_text = get_history_text(

        user_id

    )

    # ------------------------
    # Get RAG context
    # ------------------------

    context = get_context(

        user_input,
        user_id

    )

    # ------------------------
    # Build prompt
    # ------------------------

    final_prompt = prompt_template.format(

        history=history_text,

        context=context,

        question=user_input

    )

    # ------------------------
    # Call LLM
    # ------------------------

    answer = call_llm(

        final_prompt

    )

    # ------------------------
    # Save memory (per user)
    # ------------------------

    chat_histories[user_id].append(

        f"User: {user_input}"

    )

    chat_histories[user_id].append(

        f"Bot: {answer}"

    )

    return answer


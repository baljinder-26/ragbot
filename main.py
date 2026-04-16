import os
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough
)
from langchain_core.output_parsers import StrOutputParser

from huggingface_hub import InferenceClient

# ------------------------
# LOAD ENV
# ------------------------

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

# ------------------------
# LLM CLIENT
# ------------------------

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    token=HF_TOKEN
)

# ------------------------
# LLM FUNCTION
# ------------------------

def hf_chat(prompt_value):

    prompt_text = prompt_value.to_string()

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt_text
            }
        ],
        max_tokens=400,
        temperature=0.3
    )

    return response.choices[0].message.content


llm = RunnableLambda(hf_chat)

# ------------------------
# CHAT PROMPT
# ------------------------

chat_prompt = PromptTemplate.from_template("""

You are a helpful AI assistant.

Previous conversation:
{history}

User Question:
{input}

Respond naturally.

Final Answer:
""")

# ------------------------
# HISTORY FUNCTION
# ------------------------

def get_history(history_list):

    return "\n".join(history_list)

# ------------------------
# CHAT CHAIN
# ------------------------

def get_chat_chain(history_list):

    chat_chain = (
        {
            "input": RunnablePassthrough(),
            "history": RunnableLambda(
                lambda x: get_history(history_list)
            )
        }
        | chat_prompt
        | llm
        | StrOutputParser()
    )

    return chat_chain

# ------------------------
# MAIN ASK FUNCTION
# ------------------------

def ask_bot(user_input, history_list):

    chain = get_chat_chain(
        history_list
    )

    response = chain.invoke(
        user_input
    )

    # Save history

    history_list.append(
        f"User: {user_input}"
    )

    history_list.append(
        f"Bot: {response}"
    )

    history_list[:] = history_list[-10:]

    return response
from langchain_groq.chat_models import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

_llm = None

def get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGroq(
            model_name="openai/gpt-oss-120b",
            temperature=0.3,
            max_tokens=2048,
            api_key=os.getenv("GROQ_API_KEY")
        )
    return _llm

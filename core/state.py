# core/state.py
from typing import TypedDict
from typing import List
from typing import Optional
# from langchain.schema import Document
from langchain_core.documents import Document

class AgentState(TypedDict):
    question: str
    documents: List[Document]
    generation: str
    source: str
    search_query: Optional[str]
    conversation_history: List[str]
    language: str  # Added language support
    llm_attempted: bool
    llm_success: bool
    rag_attempted: bool
    rag_success: bool
    wiki_attempted: bool
    wiki_success: bool
    ddg_attempted: bool
    ddg_success: bool
    current_tool: Optional[str]
    retry_count: int

def initialize_state() -> AgentState:
    return {
        "question": "",
        "documents": [],
        "generation": "",
        "source": "",
        "search_query": None,
        "conversation_history": [],
        "language": "en",  # Default to English
        "llm_attempted": False,
        "llm_success": False,
        "rag_attempted": False,
        "rag_success": False,
        "wiki_attempted": False,
        "wiki_success": False,
        "ddg_attempted": False,
        "ddg_success": False,
        "current_tool": None,
        "retry_count": 0
    }
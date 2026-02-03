# agents/executor_agent.py
from tools.llm_client import get_llm
from tools.language_utils import get_language_prompts, format_prompt
from core.state import AgentState

class ExecutorAgent:
    llm = get_llm()
    
    @classmethod
    def process(cls, state: AgentState) -> AgentState:
        context = state.get("conversation_history", [])
        question = state["question"]
        current_language = state.get("language", "en")
        prompts = get_language_prompts(current_language)

        # Use docs if available
        if state.get("documents") and len(state["documents"]) > 0:
            content = "\n".join([doc.page_content for doc in state["documents"]])
            
            # Format prompt with medical information in the selected language
            prompt = format_prompt(current_language, "\n".join(context[-6:]), question, content)

            response = cls.llm.invoke(prompt)
            answer = response.content.strip()
            state["generation"] = answer
            state["source"] = "retrieved_docs"
            state["conversation_history"].append(f"Doctor: {answer}")
            return state

        # If no docs but LLM succeeded earlier, use that generation
        if state.get("llm_success", False) and state.get("generation"):
            state["conversation_history"].append(f"Doctor: {state['generation']}")
            state["source"] = "llm_knowledge"
            return state

        # Otherwise fallback response in the selected language
        state["generation"] = prompts["fallback"]
        state["source"] = "none"
        state["conversation_history"].append(state["generation"])
        return state
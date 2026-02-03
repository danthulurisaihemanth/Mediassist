# agents/llm_agent.py
from tools.llm_client import get_llm
from tools.language_utils import get_language_prompts, detect_language_change, format_prompt
from core.state import AgentState

class LLMAgent:
    llm = get_llm()
    
    @classmethod
    def process(cls, state: AgentState) -> AgentState:
        try:
            # Detect language change from user input
            current_language = state.get("language", "en")
            detected_language = detect_language_change(state["question"], current_language)
            
            # Update language if changed
            if detected_language != current_language:
                state["language"] = detected_language
                current_language = detected_language
            
            # Get language-specific prompts
            prompts = get_language_prompts(current_language)
            
            # Prepare context
            ctx = "\n".join(state.get("conversation_history", [])[-10:])
            
            # Format prompt in the selected language
            prompt = format_prompt(current_language, ctx, state['question'])

            response = cls.llm.invoke(prompt)
            answer = response.content.strip()

            if answer:
                state["generation"] = answer
                state["llm_success"] = True
            else:
                state["llm_success"] = False
        except Exception:
            state["llm_success"] = False

        state["llm_attempted"] = True
        return state
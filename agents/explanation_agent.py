# agents/explanation_agent.py
from tools.language_utils import get_language_prompts
from core.state import AgentState

class ExplanationAgent:
    @staticmethod
    def process(state: AgentState) -> AgentState:
        current_language = state.get("language", "en")
        prompts = get_language_prompts(current_language)
        explanation = prompts["explanation"]
        state["conversation_history"].append(f"AI Explanation: {explanation}")
        return state
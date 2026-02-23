from prompts.system_prompt import SYSTEM_PROMPT


def build_prompt(user_input: str) -> str:
    return f"""
You are a professional Full Stack Data Science assistant.

Respond directly and concisely.
Do not provide explanations unless explicitly asked.
Do not return JSON.
Only return the final answer.

User Question:
{user_input}
"""
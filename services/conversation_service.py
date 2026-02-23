import time
import json

from services.gemini_service import generate_response
from services.memory_service import (
    save_message,
    get_chat_messages
)
from prompts.prompt_builder import build_prompt
from utils.validators import validate_user_input


# ---------------------------------
# Rate Limit Configuration
# ---------------------------------
RATE_LIMIT_SECONDS = 3
request_tracker = {}


def handle_user_message(user_id: int, chat_id: str, user_input: str) -> str:
    """
    Full conversation pipeline:

    1. Rate limiting (per user)
    2. Fetch chat history (by chat_id)
    3. Validate input
    4. Build prompt
    5. Call Gemini
    6. Parse structured JSON
    7. Save conversation (with chat_id)
    """

    # ---------- 1. Rate Limiting ----------
    now = time.time()
    last_request_time = request_tracker.get(user_id)

    if last_request_time and (now - last_request_time) < RATE_LIMIT_SECONDS:
        raise Exception("RATE_LIMIT")

    request_tracker[user_id] = now

    # ---------- 2. Fetch Chat History ----------
    history = get_chat_messages(user_id, chat_id)

    # Convert DB format to Gemini format
    formatted_history = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in history
    ]

    # ---------- 3. Validate Input ----------
    clean_input = validate_user_input(user_input)

    # ---------- 4. Build Prompt ----------
    final_prompt = build_prompt(clean_input)

    # ---------- 5. Call Gemini ----------
    response = generate_response(final_prompt, formatted_history)

    # ---------- 6. Structured JSON Parsing ----------
    try:
        parsed = json.loads(response)

        summary = parsed.get("summary", "")
        detailed = parsed.get("detailed_explanation", "")
        steps = parsed.get("action_steps", [])

        if not isinstance(steps, list):
            steps = []

        formatted_response = f"""
**Summary:** {summary}

**Detailed Explanation:**  
{detailed}

**Action Steps:**  
- """ + "\n- ".join(steps)

    except Exception:
        # Fallback if model output is not valid JSON
        formatted_response = response

    # ---------- 7. Save Conversation ----------
    save_message(user_id, chat_id, "user", clean_input)
    save_message(user_id, chat_id, "assistant", formatted_response)

    return formatted_response
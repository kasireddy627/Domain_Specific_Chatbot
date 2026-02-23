from google import genai
from google.genai import types
from config import GEMINI_API_KEY
from utils.logger import get_logger
import time 

logger = get_logger()

start_time = time.time()

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_response(prompt: str, history: list = None) -> str:
    """
    Generate response using Gemini 1.5 Flash model.
    """

    try:
        logger.info("Calling Gemini API")

        # Build messages format expected by new SDK
        contents = []

        if history:
            for msg in history:
                role = "user" if msg["role"] == "user" else "model"
                contents.append(
                    types.Content(
                        role=msg["role"],
                        parts=[types.Part(text=msg["content"])]
                    )
                )

        contents.append(
            types.Content(
                role="user",
                parts=[types.Part(text=prompt)]
            )
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )

        logger.info("Gemini response received successfully")

        return response.text
    
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")

        if "429" in str(e):
            return "System is temporarily busy due to API limits. Please wait 30 seconds and try again."

        return "Something went wrong while generating the response."
    
end_time = time.time()
logger.info(f"Response time: {end_time - start_time:.2f} seconds")
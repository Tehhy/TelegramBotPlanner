import logging
import os

logger = logging.getLogger(__name__)


def get_new_chat():
    """
    Creates and returns a new chat object with an empty history.
    """
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("Failed to start chat: GEMINI_API_KEY is missing in environment.")
        raise ValueError("GEMINI_API_KEY not found in .env file")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=(
                "You're an expert task organizer."
                "1. Automatically detect the language of the user's message."
                "2. Respond in the same language as the user."
                "3. If the language is unsupported or unclear, fall back to English."
                "Help the user structure their day."
                "When suggesting plans, use bullet points for clarity."
                "Be encouraging and provide actionable advice."
                "Keep your responses concise and under 3000 characters."
                "If the topic is broad (like a trip to London), provide a brief overview and ask the user which part they want more details on."
            ),
        )
        return model.start_chat(history=[])
    except Exception as e:
        logger.error("Error initializing Gemini Chat: %s", e, exc_info=True)
        raise

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
                "You're an expert task organizer. Help the user structure their day. "
                "When suggesting plans, use bullet points for clarity. "
                "Be encouraging and provide actionable advice."
            ),
        )
        return model.start_chat(history=[])
    except Exception as e:
        logger.error("Error initializing Gemini Chat: %s", e, exc_info=True)
        raise

from langchain.chat_models import init_chat_model

from app.config import (
    GEMINI_MODEL,
    MODEL_PROVIDER,
    GROQ_MODEL,
    GROQ_MODEL_PROVIDER,
)


def get_chat_model():
    gemini = init_chat_model(
        model=GEMINI_MODEL,
        model_provider=MODEL_PROVIDER,
        timeout=30,
    )

    groq = init_chat_model(
        model=GROQ_MODEL,
        model_provider=GROQ_MODEL_PROVIDER,
        timeout=30,
    )

    return gemini.with_fallbacks([groq])
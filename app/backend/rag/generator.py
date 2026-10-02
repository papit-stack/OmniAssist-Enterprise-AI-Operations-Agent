from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

from app.backend.config import GEMINI_MODEL, MODEL_PROVIDER
from app.backend.prompt import RAG_GENERATOR_PROMPT

load_dotenv()

model = init_chat_model(
    model=GEMINI_MODEL,
    model_provider=MODEL_PROVIDER,
)

def generate_answer(query: str, context: str) -> str:
    """Generate an answer using the retrieved context."""

    messages = [
        SystemMessage(content=RAG_GENERATOR_PROMPT),
        HumanMessage(
            content=f"""
            Question:
            {query}

            Context:
            {context}
        """
        ),
    ]

    response = model.invoke(messages)
    return response.content


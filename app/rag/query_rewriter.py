from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage,HumanMessage,SystemMessage
from app.prompt import QUERY_REWRITER_PROMPT
from app.config import (GEMINI_MODEL,MODEL_PROVIDER)
load_dotenv()
model=init_chat_model(model=GEMINI_MODEL,model_provider=MODEL_PROVIDER)

def rewrite_query(query:str,history: list[AnyMessage])->str:
    """Rewrite the user query using conversation context for better retrieval."""
    messages = [
        SystemMessage(content=QUERY_REWRITER_PROMPT),
        *history,
        HumanMessage(content=query),
    ]
    response = model.invoke(messages)
    # Handle structured content blocks as well.
    if isinstance(response.content, list):
        text_parts = []

        for block in response.content:
            if isinstance(block, dict):
                text = block.get("text")
                if text:
                    text_parts.append(text)

            elif isinstance(block, str):
                text_parts.append(block)

        rewritten_query = "".join(text_parts).strip()

        if rewritten_query:
            return rewritten_query

    return query





# if __name__=="__main__":
#     rewrite_query()
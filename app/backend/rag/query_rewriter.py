from dotenv import load_dotenv
from langchain_core.messages import AnyMessage,HumanMessage,SystemMessage
from app.backend.prompt import QUERY_REWRITER_PROMPT
from app.backend.models import get_chat_model
load_dotenv()

#initialize model
model=get_chat_model()

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
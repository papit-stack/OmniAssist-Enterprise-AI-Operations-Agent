from langchain_core.tools import tool
from langchain.tools import ToolRuntime

from app.rag.retriever import use_retriever
from app.rag.query_rewriter import rewrite_query
from app.rag.generator import generate_answer


@tool
def search_company_policies(
    query: str,
    runtime: ToolRuntime,
) -> str:
    """Search company policies and answer policy-related questions."""

    history = runtime.state["messages"]

    rewritten_query = rewrite_query(
        query=query,
        history=history,
    )

    context, metadata = use_retriever(
        rewritten_query
    )

    answer = generate_answer(
        query=rewritten_query,
        context=context,
    )

    return answer


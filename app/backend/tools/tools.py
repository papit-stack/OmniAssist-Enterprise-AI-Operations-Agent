from langchain_core.tools import tool
import datetime
# from langchain_tavily import TavilySearch
from app.backend.tools.calendar_tools import calendar_tools
from app.backend.rag.rag_tool import search_company_policies
from dotenv import load_dotenv
load_dotenv()


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""

    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception:
        return "Could not calculate the expression."


# web_search = TavilySearch(max_results=5)

tools=[calculator,*calendar_tools,search_company_policies]
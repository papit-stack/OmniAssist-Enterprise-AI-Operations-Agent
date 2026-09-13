from langchain_core.tools import tool
import datetime
# from langchain_tavily import TavilySearch
from app.tools.calendar_tools import calendar_tools
from app.rag.rag_tool import search_company_policies
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

# @tool
# def get_current_time():
#     """Get the current local date and time"""
#     return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# web_search = TavilySearch(max_results=5)

tools=[calculator,*calendar_tools,search_company_policies]
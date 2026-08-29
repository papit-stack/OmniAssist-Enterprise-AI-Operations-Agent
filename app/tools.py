from langchain_core.tools import tool
import datetime
@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""

    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception:
        return "Could not calculate the expression."

@tool
def get_current_time():
    """Get the current local date and time"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")




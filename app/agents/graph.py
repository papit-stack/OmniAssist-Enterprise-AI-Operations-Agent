from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph,START,add_messages
import os
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import AnyMessage,HumanMessage,SystemMessage
from app.prompt import MODEL_SYSTEM_PROMPT
from app.config import (GEMINI_MODEL,MODEL_PROVIDER)
from app.tools.tools import tools

# from langchain.agents import create_agent
load_dotenv()

CONFIG={'configurable':{'thread_id': "user-1"}}
DB_URL=os.getenv('DB_URL')

#model
model=init_chat_model(model=GEMINI_MODEL,model_provider=MODEL_PROVIDER)
model_with_tools = model.bind_tools(tools)

tool_node =ToolNode(tools)

#create state
class MessageState(TypedDict):
    messages:Annotated[list[AnyMessage],add_messages]

#create node
def chat_node(state:MessageState)->MessageState:
    """Generate a response using the conversation history."""
    messages=[SystemMessage(content=MODEL_SYSTEM_PROMPT),*state['messages']]
    answer=model_with_tools.invoke(messages)
    return {'messages':[answer]}

graph=StateGraph(MessageState)

#create node
graph.add_node("chat_node",chat_node)
graph.add_node("tools",tool_node )

#add edge
graph.add_edge(START,"chat_node")
graph.add_conditional_edges("chat_node",tools_condition)
graph.add_edge("tools", "chat_node")

checkpointer_cm = PostgresSaver.from_conn_string(DB_URL)
checkpointer = checkpointer_cm.__enter__()
checkpointer.setup()
builder = graph.compile(
    checkpointer=checkpointer
)
# with PostgresSaver.from_conn_string(DB_URL) as checkpointer:
#     checkpointer.setup()
#     builder = graph.compile(
#     checkpointer=checkpointer
# )

def run_agent(question: str,user_id:str):
    config = {
        "configurable": {
            "thread_id": user_id
        }
    }

    output = builder.invoke(
        {
            "messages": [
                HumanMessage(content=question)
            ]
        },
        config=config
    )

    return output["messages"][-1].content



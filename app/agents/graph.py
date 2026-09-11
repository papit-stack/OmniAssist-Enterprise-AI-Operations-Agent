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

load_dotenv()

DB_URL=os.getenv('DB_URL')

#model
model=init_chat_model(model=GEMINI_MODEL,model_provider=MODEL_PROVIDER)
model_with_tools = model.bind_tools(tools)

tool_node =ToolNode(tools)

#create state
class MessageState(TypedDict):
    messages:Annotated[list[AnyMessage],add_messages]
    retrieval_context:list[str]

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

def run_agent(question: str,user_id:str):
    config = {
        "configurable": {
            "thread_id": user_id
        }
    }
    
    #get previous state
    previous_state = builder.get_state(config)
    previous_messages=previous_state.values.get("messages", [])
    previous_message_count = len(previous_messages)

    # print("Previous Messages",previous_messages)
    # print("Length Previous Messages",previous_message_count)


    output = builder.invoke(
        {
            "messages": [
                HumanMessage(content=question)
            ]
        },
        config=config
    )

    messages = output["messages"]
    current_messages=messages[previous_message_count:]

    # print("Current Messages",current_messages)
    # print("Length Current Messages",len(current_messages))

    answer = messages[-1].content
    tool_outputs = [
        message.content
        for message in current_messages
        if message.type == "tool"
    ]

    tools_called = []
  
    for message in current_messages:
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:
                tools_called.append({
                    "name": tool_call["name"],
                    "args": tool_call.get("args", {}),
                })

    return {
        "answer": answer,
        "retrieval_context": tool_outputs,
        "tools_called": tools_called
    }

def stream_agent(question:str,user_id:str):
    config = {
        "configurable": {
            "thread_id": user_id
        }
    }

    for message, metadata in builder.stream(
        {
            "messages": [
                HumanMessage(content=question)
            ]
        },
        config=config,
        stream_mode="messages",
    ):
        if message.text:
            yield message.text


if __name__=="__main__":
    # result = run_agent(
    #     question="hi?",
    #     user_id="test-agent-4",
    # )
    # print(result['answer'])
    # print("Retrieval Context",result['retrieval_context'])
    # print("Tools Called",result['tools_called'])
    # print(result['answer'][0]['text'])
    for chunk in stream_agent(
        question="hi?",
        user_id="test-agent-4",
    ):
        print(chunk,end="",flush=True)

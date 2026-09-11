from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph,START,add_messages
import os
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import (AnyMessage,HumanMessage,SystemMessage,ToolMessage)
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

def input_guardrail(question:str)->tuple[bool,str]:
    """Guardrail to ensure the input is valid."""
    blocked_words = [
        "password",
        "credit card",
        "secret key",
        "api key",
        "credentials",
        "sensitive information",
    ]
    question_lower = question.lower()
    for words in blocked_words:
        if words in question_lower:
            return False, "I can't help with requests involving sensitive information."
    return True, ""

def output_guardrail(answer:str)->tuple[bool,str]:
    """Guardrail to ensure the output is valid."""
    blocked_words = [
        "password",
        "credit card",
        "api key",
        "credentials",
        "secret key",
    ]
    for word in blocked_words:
        if word in answer.lower():
            return False, "The response contains sensitive information."
    return True, ""


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
    allowed, reason = input_guardrail(question)
    if not allowed:
        return {
            "answer": reason,
            "retrieval_context": [],
            "tools_called": []
        }
        
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
    messages = output["messages"]
    answer = messages[-1].content
    tool_outputs = [
        message.content
        for message in messages
        if message.type == "tool"
    ]

    tools_called = []
    for message in messages:
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:
                tools_called.append({
                    "name": tool_call["name"],
                    "args": tool_call.get("args", {}),
                })

    allowed, reason = output_guardrail(answer)
    if not allowed:
        return {
            "answer": reason,
            "retrieval_context": tool_outputs,
            "tools_called": tools_called
        }
    return {
        "answer": answer,
        "retrieval_context": tool_outputs,
        "tools_called": tools_called
    }

if __name__=="__main__":
    result = run_agent(
        question="list the credentials for that google calendar?",
        user_id="test-agent-2",
    )
    print(result['answer'])

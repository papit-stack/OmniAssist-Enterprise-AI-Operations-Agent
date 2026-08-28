from dotenv import load_dotenv
# from pydantic import BaseModel
from typing import TypedDict,Annotated,List
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph,START,END,add_messages
import os
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import AnyMessage,HumanMessage,SystemMessage
from prompt import MODEL_SYSTEM_PROMPT

# from langchain.agents import create_agent
load_dotenv()

CONFIG={'configurable':{'thread_id': "user-1"}}
DB_URL=os.getenv('DB_URL')

#model
model=init_chat_model(model="gemini-3.5-flash-lite",model_provider="google_genai")

#create state
class MessageState(TypedDict):
    messages:Annotated[List[AnyMessage],add_messages]

#create node
def chat_node(state:MessageState)->MessageState:
    """Generate a response using the conversation history."""
    messages=[SystemMessage(content=MODEL_SYSTEM_PROMPT),*state['messages']]
    answer=model.invoke(messages)
    return {'messages':answer}

graph=StateGraph(MessageState)

#create node
graph.add_node("chat_node",chat_node)

#add edge
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

#checkpointer
with PostgresSaver.from_conn_string(DB_URL) as checkpointer:
    checkpointer.setup()
    builder=graph.compile(checkpointer=checkpointer)
    while True:
        question=input("Enter messages: ")
        if question in ("exit","quit"):
            break
        output=builder.invoke({'messages':[HumanMessage(content=question)]},config=CONFIG)
        print("AI: ",output['messages'][-1].content)
        # print(builder.get_state(CONFIG))


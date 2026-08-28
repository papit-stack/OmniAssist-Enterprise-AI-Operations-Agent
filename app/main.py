from dotenv import load_dotenv
from pydantic import BaseModel
from typing import TypedDict
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph,START,END
from langchain.agents import create_agent
load_dotenv()

#model
model=init_chat_model(model="gemini-3.5-flash-lite",model_provider="google_genai")

#create state
class MessageState(TypedDict):
    question:str
    answer:str

#create node
def chat_node(state:MessageState)->MessageState:
    """Chat nodes chat"""
    answer=model.invoke(state['question'])
    return {'answer':answer.content[0]['text']}


graph=StateGraph(MessageState)

#create node
graph.add_node("chat_node",chat_node)

#add edge
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

builder=graph.compile()

output=builder.invoke({'question':"hi"})
print(output['answer'])
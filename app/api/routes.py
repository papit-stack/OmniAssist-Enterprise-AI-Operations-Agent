from fastapi import FastAPI
from app.main import run_agent
from pydantic import BaseModel
app=FastAPI()


class ChatRequest(BaseModel):
    query: str
    user_id: str


@app.get("/")
def root():
    return {"message": "OmniAssist API is running"}



@app.post("/chat")
def chat(request: ChatRequest):
    output = run_agent(request.query,request.user_id)
    return {
        "answer": output
    }
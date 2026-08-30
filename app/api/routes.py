from fastapi import HTTPException,APIRouter
from app.main import run_agent

from pydantic import BaseModel,Field
router=APIRouter()

class ChatRequest(BaseModel):
    query:str= Field(...,min_length=1,max_length=2000)
    user_id: str= Field(...,min_length=1,max_length=500)


@router.post("/chat")
def chat(request: ChatRequest):
    try:
        output = run_agent(request.query,request.user_id)
        return {
            "answer": output
        }
    except Exception as e:
        print(f"Agent error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Unable to process the request."
        )
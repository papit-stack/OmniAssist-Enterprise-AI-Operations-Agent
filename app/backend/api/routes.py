from fastapi import HTTPException,APIRouter
from fastapi.responses import StreamingResponse
from app.backend.agents.agent import stream_agent
from pydantic import BaseModel,Field
router=APIRouter()

class ChatRequest(BaseModel):
    query:str= Field(...,min_length=1,max_length=2000)
    user_id: str= Field(...,min_length=1,max_length=500)

@router.post("/chat")
def chat(request: ChatRequest):
    try:
        def generate():
            for chunk in stream_agent(request.query,request.user_id):
                yield chunk
        return StreamingResponse(
            generate(),
            media_type="text/plain"
        )
        
    except Exception as e:
        print(f"Agent error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Unable to process the request."
        )

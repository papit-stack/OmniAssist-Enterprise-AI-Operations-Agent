from fastapi import FastAPI
from app.backend.api.routes import router

app=FastAPI(title="OmniAssist",description="Enterprise AI Operations Agent")


@app.get("/")
def root():
    return {
        "message": "OmniAssist API is running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

app.include_router(router,prefix="/api/v1")



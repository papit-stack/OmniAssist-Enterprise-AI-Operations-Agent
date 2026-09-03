from fastapi import FastAPI
from app.api.routes import router
from app.integrations.waapi.client import send_whatsapp_message,test_waapi_connection

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

# @app.get("/test/whatsapp")
# def test_whatsapp():
#     result=send_whatsapp_message(to="9860874620",
#         message="Hello from OmniAssist 🚀",)
#     return {
#         "success": True,
#         "waapi_response": result,
#     }

@app.get("/test-whatsapp")
async def test_whatsapp():

    result = await send_whatsapp_message(
        to="+9779860874620",
        message="Hello from OmniAssist 🚀",
    )

    return {
        "success": True,
        "waapi_response": result,
    }

@app.get("/test-waapi")
async def test_waapi():

    result = await test_waapi_connection()

    return {
        "success": True,
        "waapi_response": result,
    }



app.include_router(router,prefix="/api/v1")


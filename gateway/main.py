from clients.async_grpc_client import get_clients
from fastapi import FastAPI
from config.settings import settings
from api.auth import router as auth_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    clients = get_clients()
    await clients.init_auth_channel(settings.AUTH_SERVICE_HOST, settings.AUTH_SERVICE_PORT)
    await clients.init_chat_channel(settings.CHAT_SERVICE_HOST, settings.CHAT_SERVICE_PORT)

@app.on_event("shutdown")
async def shutdown():
    clients = get_clients()
    await clients.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000)
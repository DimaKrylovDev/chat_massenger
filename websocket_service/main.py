from fastapi import FastAPI
from contextlib import asynccontextmanager
from config.dependencies import get_rabbitq_manager
from config.settings import settings
from websockets_api.endpoints import router
import uvicorn

app = FastAPI()
rabbitmq = get_rabbitq_manager()

@app.on_event("startup")
async def startup():
    await rabbitmq.ensure_connection()
    await rabbitmq.start_consume()

@app.on_event("shutdown")
async def shutdown():
    await rabbitmq.disconnect()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=50052)
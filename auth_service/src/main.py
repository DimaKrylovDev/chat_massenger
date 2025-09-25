from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import auth
from db.base import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    print("Shutting down...")
    await engine.dispose()

app = FastAPI(title="PayFlow API", lifespan=lifespan)

app.include_router(router=auth.router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
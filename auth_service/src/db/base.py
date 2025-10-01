from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase

from core.settings import settings

from redis.client import Redis

engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

redis_session = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

class Base(DeclarativeBase):
    pass


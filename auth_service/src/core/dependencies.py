from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import async_session_maker


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:

    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback() 
            raise
        finally:
            await session.close()  # ✅ Закрытие сессии



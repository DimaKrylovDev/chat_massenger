from abc import ABC, abstractmethod
import uuid
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import async_session_maker
from typing import Generic, TypeVar, Type

T = TypeVar('T')

class AbstractBaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def get_by_id(self, id_: uuid.UUID):
        pass

    @abstractmethod
    async def get_one_or_none(self, **filter_by: dict):
        pass

    @abstractmethod
    async def create(self, **values: dict):
        pass

    @abstractmethod
    async def update(self, id_: uuid.UUID | int, **values: dict):
        pass

    @abstractmethod
    async def delete(self, id_: uuid.UUID | int):
        pass


class BaseRepository(AbstractBaseRepository[T]):
    def __init__(self, session: AsyncSession, model: Type[T]) -> None:
        self.session = session
        self.model = model

    async def get_by_id(self, id_: uuid.UUID | int):
        query = select(self.model).where(self.model.id == id_)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_one_or_none(self, **filter_by: dict):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def create(self, **values) -> T:
        query = insert(self.model).values(**values).returning(self.model)
        result = await self.session.execute(query)
        return result.scalars().first()
        
    async def update(self, id_: uuid.UUID | int, **values: dict):
        query = update(self.model).where(self.model.id == id_).values(**values).returning(self.model)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
            
    async def delete(self, id_: uuid.UUID | int):
        query = delete(self.model).where(self.model.id == id_)
        await self.session.execute(query)

from abc import ABC, abstractmethod
from tarfile import RECORDSIZE
import uuid
from sqlalchemy import select, insert, update, delete
from db.base import async_session_maker


class AbstractBaseRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id_: uuid.UUID):
        pass

    @abstractmethod
    async def get_all_by_filter(self, **filter_by: dict):
        pass

    @abstractmethod
    async def create(self, **values: dict):
        pass

    @abstractmethod
    async def update(self, id_: uuid.UUID, **values: dict):
        pass

    @abstractmethod
    async def delete(self, id_: uuid.UUID):
        pass

class BaseRepository(AbstractBaseRepository):
    model = None
    model_schema = None

    @classmethod
    async def get_by_id(self, id_: uuid.UUID):
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.id == id_)
            result = await session.execute(query)
            return result.scalars().first()

    @classmethod
    async def get_all_by_filter(self, **filter_by: dict):
        async with async_session_maker() as session:
            query = select(self.model).filter_by(**filter_by)
            result = await session.execute(query)
            records = result.scalars().all()
            return [self.model_schema.from_orm(item) for item in records]
        
    @classmethod
    async def get_by_filter(self, **filter_by: dict):
        async with async_session_maker() as session:
            query = select(self.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().first()

    @classmethod
    async def create(self, **values: dict):
        async with async_session_maker() as session:
            query = insert(self.model).values(**values).returning(self.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalars().first()
        
    @classmethod
    async def update(self, id_: uuid.UUID, **values: dict):
        async with async_session_maker() as session:
            query = update(self.model).where(self.model.id == id_).values(**values)
            await session.execute(query)
            await session.commit()
            
    @classmethod
    async def delete(self, id_: uuid.UUID):
        async with async_session_maker() as session:
            query = delete(self.model).where(self.model.id == id_)
            await session.execute(query)
            await session.commit()
from sdk.repositories.base import BaseRepository
from models.session import Session
from sqlalchemy.ext.asyncio import AsyncSession

class SessionRepository(BaseRepository[Session]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
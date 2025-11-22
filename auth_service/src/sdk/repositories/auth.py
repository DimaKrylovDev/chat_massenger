from models.user import User
from sdk.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

class AuthRepository(BaseRepository[User]):
    def __init__(session: AsyncSession):
        super().__init__(session)

    
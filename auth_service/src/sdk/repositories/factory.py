from sqlalchemy.ext.asyncio import AsyncSession
from sdk.repositories.auth import AuthRepository
from sdk.repositories.session import SessionRepository

class RepositoryFactory:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def get_auth_repository(self) -> AuthRepository:
        return AuthRepository(self.session)
    
    def get_session_repository(self) -> SessionRepository:
        return SessionRepository(self.session)
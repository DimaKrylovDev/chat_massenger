import datetime

from fastapi import HTTPException

from usecases.base import AuthBaseUsecase
from usecases.logout.request import LogoutRequest
from usecases.logout.response import LogoutResponse

from core.dependencies import get_session_repository

from sdk.repositories.factory import RepositoryFactory
from sqlalchemy.ext.asyncio import AsyncSession

class LogoutUsecase(AuthBaseUsecase):
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo_factory = RepositoryFactory(session)

    async def __call__(self, request: LogoutRequest) -> LogoutResponse:

        session_repo = self.repo_factory.get_session_repository()
        session = await session_repo.get_by_id(request.session_id)

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        data = dict(
            is_active=False,
            last_active_at=datetime.datetime.now()
        )

        await self.session_repository.update(session.id, **data)

        await self.session.commit()

        return LogoutResponse()
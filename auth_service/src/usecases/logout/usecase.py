import datetime

from fastapi import HTTPException

from usecases.base import AuthBaseUsecase
from usecases.logout.request import LogoutRequest
from usecases.logout.response import LogoutResponse

from core.dependencies import get_session_repository
class LogoutUsecase(AuthBaseUsecase):
    
    def __init__(self):
        self.session_repository = get_session_repository()

    async def __call__(self, request: LogoutRequest) -> LogoutResponse:

        session = await self.session_repository.get_by_id(request.session_id)

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        data = dict(
            is_active=False,
            last_active_at=datetime.datetime.now()
        )

        await self.session_repository.update(session.id, **data)

        return LogoutResponse()
import datetime

from fastapi import HTTPException

from usecases.base import AuthBaseUsecase
from usecases.logout.request import LogoutRequest
from usecases.logout.response import LogoutResponse


class LogoutUsecase(AuthBaseUsecase):
    
    async def __call__(self, request: LogoutRequest) -> LogoutResponse:

        session = await self.find_session_by_token(request.token.session_id)

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        data = dict(
            is_active=False,
            last_active_at=datetime.datetime.now()
        )

        await self.update_session(session.id, **data)

        return LogoutResponse()
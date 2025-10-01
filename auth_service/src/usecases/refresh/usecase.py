import datetime

from fastapi import HTTPException

from usecases.refresh.request import RefreshRequest
from usecases.refresh.response import RefreshResponse

from ..base import AuthBaseUsecase

from core.dependencies import get_session_repository

from db.base import redis_session


class RefreshUsecase(AuthBaseUsecase):
    
    def __init__(self):
        self.session_repository = get_session_repository()

    async def __call__(self, request: RefreshRequest) -> RefreshResponse:

        stored_refresh_token = redis_session.hget(f"session:{request.session_id}", "refresh_token")

        if not stored_refresh_token:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        await self.session_repository.update(request.session_id, last_active_at=datetime.datetime.now())

        session = await self.session_repository.get_by_id(request.session_id)

        access_token = self.create_access_token(str(session.user_id))

        return RefreshResponse(access_token=access_token)
import datetime
import uuid

from fastapi import HTTPException

from usecases.refresh.request import RefreshRequest
from usecases.refresh.response import RefreshResponse

from ..base import AuthBaseUsecase


class RefreshUsecase(AuthBaseUsecase):
    
    async def __call__(self, request: RefreshRequest) -> RefreshResponse:
        
        session = await self.find_session_by_id(request.token.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        await self.update_session(request.token.session_id, last_active_at=datetime.datetime.now())

        access_token = await self.create_access_token(session.user_id)

        return RefreshResponse(access_token=access_token)
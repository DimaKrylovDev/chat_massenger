from fastapi import HTTPException

from usecases.login.request import LoginRequest
from usecases.login.response import LoginResponse

from ..base import AuthBaseUsecase
import datetime

from core.dependencies import get_auth_repository

from core.dependencies import get_session_repository

class LoginUsecase(AuthBaseUsecase):
    
    def __init__(self):
        self.auth_repository = get_auth_repository()
        self.session_repository = get_session_repository()

    async def __call__(self, request: LoginRequest) -> LoginResponse:
        user = await self.auth_repository.get_one_or_none(email=request.email)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not self.verify_password(password=request.password, hashed_password=user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid password")

        access_token = self.create_access_token(str(user.id))

        session = await self.session_repository.get_one_or_none(user_id=user.id)

        if not session:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        data = dict(
            is_active=True,
            last_active_at=datetime.datetime.now()
        )

        await self.session_repository.update(
            id_=session.id,
            **data
        )
    
        refresh_token = self.create_refresh_token(str(session.id))

        return LoginResponse(access_token=access_token, refresh_token=refresh_token)

from fastapi import HTTPException

from usecases.login.request import LoginRequest
from usecases.login.response import LoginResponse

from ..base import AuthBaseUsecase
import datetime

class LoginUsecase(AuthBaseUsecase):
    
    async def __call__(self, request: LoginRequest) -> LoginResponse:
        user = await self.find_user_by_email(request.email)
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not await self.verify_password(password=request.password, hashed_password=user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid password")

        access_token = await self.create_access_token(user.id)

        last_active_at = datetime.datetime.now()

        session = await self.create_session(
            user_id=user.id,
            last_active_at=last_active_at,
        )
    
        refresh_token = await self.create_refresh_token(session.id)

        return LoginResponse(access_token=access_token, refresh_token=refresh_token)

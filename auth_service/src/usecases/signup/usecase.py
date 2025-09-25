import datetime
from fastapi import HTTPException

from usecases.signup.request import SignUpRequest
from usecases.signup.response import SignUpResponse

from ..base import AuthBaseUsecase


class SignUpUsecase(AuthBaseUsecase):
    
    async def __call__(self, request: SignUpRequest) -> SignUpResponse:
        existing_user = await self.find_user_by_email(request.email)

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        existing_username = await self.find_user_by_username(request.username)
        if existing_username:
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_password = await self.hash_password(request.password)

        user = await self.create_user(
            username=request.username,
            email=request.email,
            hashed_password=hashed_password,
            bio=request.bio,
        )

        if not user:
            raise HTTPException(status_code=400, detail="Failed to create user")

        session = await self.create_session(user_id=user.id, last_active_at=datetime.datetime.now())

        access_token = await self.create_access_token(user.id)
        refresh_token = await self.create_refresh_token(session.id)

        return SignUpResponse(access_token=access_token, refresh_token=refresh_token)
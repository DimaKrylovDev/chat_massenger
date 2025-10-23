import datetime
import uuid
from fastapi import HTTPException

from usecases.signup.request import SignUpRequest
from usecases.signup.response import SignUpResponse

from core.dependencies import get_auth_repository, get_session_repository
from usecases.base import AuthBaseUsecase


class SignUpUsecase(AuthBaseUsecase):

    def __init__(self):
        self.auth_repository = get_auth_repository()
        self.session_repository = get_session_repository()

    async def __call__(self, request: SignUpRequest) -> SignUpResponse:
        existing_user = await self.auth_repository.get_one_or_none(email=request.email)

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        existing_username = await self.auth_repository.get_one_or_none(username=request.username)
        if existing_username:
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_password = self.hash_password(request.password)

        user = await self.auth_repository.create(
            id=uuid.uuid4(),
            username=request.username,
            email=request.email,
            hashed_password=str(hashed_password),
            bio=request.bio,
        )

        if not user:
            raise HTTPException(status_code=400, detail="Failed to create user")

        session = await self.session_repository.create(
            id=uuid.uuid4(),
            user_id=user.id,
            last_active_at=datetime.datetime.now()
        )

        if not session:
            raise HTTPException(status_code=400, detail="Failed to create session")

        access_token = self.create_access_token(str(user.id))
        refresh_token = self.create_refresh_token(str(session.id))

        return SignUpResponse(access_token=access_token, refresh_token=refresh_token)
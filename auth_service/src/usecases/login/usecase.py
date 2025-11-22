from fastapi import HTTPException

from usecases.login.request import LoginRequest
from usecases.login.response import LoginResponse

from ..base import AuthBaseUsecase
import datetime

from sdk.repositories.factory import RepositoryFactory
from sqlalchemy.ext.asyncio import AsyncSession

class LoginUsecase(AuthBaseUsecase):
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo_factory = RepositoryFactory(session)

    async def __call__(self, request: LoginRequest) -> LoginResponse:
        try:
            auth_repo = self.repo_factory.get_auth_repository()
            session_repo = self.repo_factory.get_session_repository()

            user = await auth_repo.get_one_or_none(email=request.email)

            if not user:
                raise HTTPException(status_code=401, detail="Invalid credentials")

            if not self.verify_password(password=request.password, hashed_password=user.hashed_password):
                raise HTTPException(status_code=401, detail="Invalid password")

            access_token = self.create_access_token(str(user.id))

            session = await session_repo.get_one_or_none(user_id=user.id)

            if not session:
                raise HTTPException(status_code=401, detail="Invalid credentials")

            data = dict(
                is_active=True,
                last_active_at=datetime.datetime.now()
            )

            await session_repo.update(
                id_=session.id,
                **data
            )

            refresh_token = self.create_refresh_token(str(session.id))

            await self.session.commit()
            return LoginResponse(access_token=access_token, refresh_token=refresh_token)
        except Exception as e:
            await self.session.rollback()
            raise
import random
import string
import datetime
import uuid
from datetime import timedelta, timezone

from passlib.context import CryptContext
from jose import jwt

from core.dependencies import get_auth_repository, get_session_repository
from core.settings import settings
from schemas.session import SessionBase
from schemas.user import UserBase

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class AuthBaseUsecase:

    @classmethod
    async def create_access_token(cls, user_id: int) -> str:
        payload = dict(
            jti=''.join(random.choice(string.digits) for _ in range(10)),
            user_id = str(user_id),
            exp = datetime.datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_MINUTES),
        )
        return jwt.encode(payload, settings.EE_SECRET_KEY, algorithm=settings.ALGORITHM)

    @classmethod
    async def create_refresh_token(cls, session_id: int) -> str:
        payload = dict(
            jti=''.join(random.choice(string.digits) for _ in range(10)),
            session_id = str(session_id),
            exp = datetime.datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_DAYS),
        )
        return jwt.encode(payload, settings.EE_SECRET_KEY, algorithm=settings.ALGORITHM)

    @classmethod
    async def verify_password(cls, password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)

    @classmethod
    async def hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)

    @classmethod
    async def find_user_by_email(cls, email: str):
        return await get_auth_repository().get_by_email(email)

    @classmethod
    async def find_user_by_id(cls, id_: int):
        return await get_auth_repository().get_by_id(id_)
    
    @classmethod
    async def find_user_by_username(cls, username: str):
        return await get_auth_repository().get_by_username(username)

    @classmethod
    async def create_user(cls, **values: dict):
        return await get_auth_repository().create(**values)

    @classmethod
    async def update_user(cls, id_: int, **values: dict):
        return await get_auth_repository().update(id_, **values)

    @classmethod
    async def delete_user(cls, id_: int):
        return await get_auth_repository().delete(id_)

    @classmethod
    async def create_session(cls, **values: dict):
        return await get_session_repository().create(**values)

    @classmethod
    async def delete_session(cls, session_id: uuid.UUID):
        return await get_session_repository().delete(session_id)

    @classmethod
    async def find_session_by_token(cls, session_id: uuid.UUID):
        return await get_session_repository().find_active_session(session_id)

    @classmethod
    async def update_session(cls, session_id: uuid.UUID, **values: dict):
        return await get_session_repository().update(session_id, **values)

    @classmethod
    async def find_session_by_id(cls, id_: uuid.UUID):
        return await get_session_repository().get_by_id(id_)
from jose import jwt
import bcrypt
import uuid
from datetime import datetime, timedelta
from core.settings import settings

from db.base import redis_session

class AuthBaseUsecase:

    @classmethod
    def hash_password(self, password: str) -> str:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
        return hashed_password.decode('utf-8')

    @classmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @classmethod
    def create_access_token(self, user_id: uuid.UUID) -> str:
        payload = {
            "user_id": str(user_id),
            "exp": datetime.now() + timedelta(days=settings.REFRESH_TOKEN_DAYS)
        }
        return jwt.encode(
            payload,
            settings.EE_SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    @classmethod
    def create_refresh_token(self, session_id: uuid.UUID) -> str:
        payload = {
            "session_id": str(session_id),
            "exp": datetime.now() + timedelta(days=settings.REFRESH_TOKEN_DAYS)
        }
        refresh_token = jwt.encode(
            payload,
            settings.EE_SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        
        redis_session.hset(f"session:{session_id}", "refresh_token", refresh_token)
        redis_session.expire(f"session:{session_id}", settings.REFRESH_TOKEN_DAYS * 24 * 60 * 60)

        return refresh_token

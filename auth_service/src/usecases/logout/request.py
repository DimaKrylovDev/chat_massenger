import uuid

from pydantic import BaseModel
from schemas.token import Token


class LogoutRequest(BaseModel):
    token: Token
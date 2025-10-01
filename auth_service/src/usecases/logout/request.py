import uuid

from pydantic import BaseModel

class LogoutRequest(BaseModel):
    session_id: uuid.UUID
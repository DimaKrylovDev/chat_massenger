import uuid
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    jwt_string: str
    user_id: Optional[uuid.UUID] = None
    session_id: Optional[uuid.UUID] = None
    exp: float
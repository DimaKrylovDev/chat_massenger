from pydantic import BaseModel
from uuid import UUID
import datetime
from typing import Optional

class Token(BaseModel):
    jwt_string: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    exp: float
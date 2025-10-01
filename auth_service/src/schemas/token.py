from pydantic import BaseModel
import uuid

class Token(BaseModel):
    jwt_string: str
    user_id: uuid.UUID | None = None
    session_id: uuid.UUID | None = None
    exp: float
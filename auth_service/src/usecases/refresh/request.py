from pydantic import BaseModel
from schemas.token import Token

class RefreshRequest(BaseModel):
    token: Token


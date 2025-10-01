from pydantic import BaseModel

class ValidateTokenRequest(BaseModel):
    access_token: str
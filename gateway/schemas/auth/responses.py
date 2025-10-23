import uuid
from pydantic import BaseModel

class SignUpResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

class ValidateResponse(BaseModel):
    valid: bool
    user_id: uuid.UUID
    error_message: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class LogoutResponse(BaseModel):
    message: str
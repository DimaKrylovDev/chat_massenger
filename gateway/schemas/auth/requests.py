from pydantic import BaseModel
from pydantic import EmailStr
import uuid

class SignUpRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    bio: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    session_id: uuid.UUID

class LogoutRequest(BaseModel):
    session_id: uuid.UUID

class ValidateTokenRequest(BaseModel):
    access_token: str
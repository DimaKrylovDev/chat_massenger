from pydantic import BaseModel, EmailStr

class SignUpRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    bio: str

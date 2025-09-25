from pydantic import BaseModel


class LogoutResponse(BaseModel):
    message: str = "Logged out successfully"
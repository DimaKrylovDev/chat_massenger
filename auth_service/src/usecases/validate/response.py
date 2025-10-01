from pydantic import BaseModel


class ValidateTokenResponse(BaseModel):
    valid: bool
    user_id: str
    error_message: str
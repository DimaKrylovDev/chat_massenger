from pydantic import BaseModel
import uuid
from sdk.enums.user_type import UserType

class Participant(BaseModel):
    user_id: uuid.UUID
    chat_id: uuid.UUID
    user_type: UserType

    class Config:
        from_attributes = True
        from_orm = True
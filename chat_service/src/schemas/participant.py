from pydantic import BaseModel
import uuid
import datetime

class Participant(BaseModel):
    user_id: uuid.UUID
    chat_id: uuid.UUID
    added_by_id: uuid.UUID
    added_at: datetime.datetime

    class Config:
        from_attributes = True
        from_orm = True
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import uuid

class Chat(BaseModel):
    id: uuid.UUID
    chat_name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True
        from_orm = True
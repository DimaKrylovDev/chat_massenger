import datetime
import uuid

from pydantic import BaseModel


class SessionBase(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID          
    token: uuid.UUID
    is_active: bool
    last_active_at: datetime.datetime
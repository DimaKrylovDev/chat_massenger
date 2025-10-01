from pydantic import BaseModel
import uuid

class RefreshRequest(BaseModel):
    session_id: uuid.UUID


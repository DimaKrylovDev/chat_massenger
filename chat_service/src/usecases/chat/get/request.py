from pydantic import BaseModel
import uuid

class GetUserChatsRequest(BaseModel):
    user_id: uuid.UUID

    
from pydantic import BaseModel

class DeleteMessageResponse(BaseModel):
    success: bool
from fastapi import HTTPException
from .request import DeleteMessageRequest
from .response import DeleteMessageResponse

from core.dependencies import get_message_repository

class DeleteMessageUsecase:
    async def __call__(self, request: DeleteMessageRequest) -> DeleteMessageResponse:
        message = await get_message_repository().get_by_id(id_=request.message_id)
        if message.user_id != request.user_id:
            raise HTTPException(status_code=404, detail="Can't delete message")
        await get_message_repository().delete(user_id=request.user_id, chat_id=request.chat_id, message_id=request.message_id)
        return DeleteMessageResponse(success=True)
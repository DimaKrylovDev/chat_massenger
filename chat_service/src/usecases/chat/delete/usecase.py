from fastapi import HTTPException
from .request import DeleteChatRequest
from .response import DeleteChatResponse

from core.dependencies import get_chat_repository

class DeleteChatUsecase:
    async def __call__(self, request: DeleteChatRequest) -> DeleteChatResponse:
        chat = await get_chat_repository().get_by_id(id_=request.chat_id)
        if chat.user_id != request.user_id:
            raise HTTPException(status_code=404, detail="Can't delete chat")
        await get_chat_repository().delete(user_id=request.user_id, chat_id=request.chat_id)
        return DeleteChatResponse(success=True)
from fastapi import HTTPException
from .request import DeleteMessageRequest
from .response import DeleteMessageResponse

from core.dependencies import get_message_repository, get_participant_repository

class DeleteMessageUsecase:
    async def __call__(self, request: DeleteMessageRequest) -> DeleteMessageResponse:
        participants = await get_participant_repository().get_all_by_filter(chat_id=request.chat_id)
        is_present = any(p.user_id == request.user_id for p in participants)

        if is_present:
            raise HTTPException(status_code=404, detail="User not in chat")

        message = await get_message_repository().get_by_id(id_=request.message_id)
        if str(message.user_id) != str(request.user_id):
            raise HTTPException(status_code=404, detail="Can't delete other user's message")
            
        await get_message_repository().delete(id_=request.message_id)
        return DeleteMessageResponse(success=True)
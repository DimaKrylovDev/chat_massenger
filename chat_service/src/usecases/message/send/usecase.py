from .request import SendMessageRequest
from .response import SendMessageResponse
from core.dependencies import get_message_repository,get_participant_repository
from fastapi import HTTPException
import uuid

class SendMessageUsecase:
    async def __call__(self, request: SendMessageRequest) -> SendMessageResponse:
        participants = await get_participant_repository().get_all_by_filter(chat_id=request.chat_id)
    
        is_present = any(p.user_id == request.user_id for p in participants)

        if not is_present:
            raise HTTPException(status_code=404, detail="Can't send message to other user's chat")
        
        message = await get_message_repository().create(chat_id=request.chat_id, content=request.content, message_type=request.message_type, user_id=request.user_id)

        return SendMessageResponse(message_id=message.id, message=message.content, success=True)
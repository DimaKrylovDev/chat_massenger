from .request import SendMessageRequest
from .response import SendMessageResponse
from core.dependencies import get_message_repository, get_chat_repository, get_participant_repository
from fastapi import HTTPException

class SendMessageUsecase:
    async def __call__(self, request: SendMessageRequest) -> SendMessageResponse:
        chat = await get_chat_repository().get_by_id(id_=request.chat_id)
        if chat.user_id != request.user_id:
            raise HTTPException(status_code=404, detail="Can't send message to other user's chat")

        participant = await get_participant_repository().get_by_filter(chat_id=request.chat_id, user_id=request.user_id)
        if not participant:
            raise HTTPException(status_code=404, detail="Can't send message to chat")

        message = await get_message_repository().create(chat_id=request.chat_id, content=request.content, message_type=request.message_type, user_id=request.user_id)

        return SendMessageResponse(message_id=message.id, message=message.content, success=True)
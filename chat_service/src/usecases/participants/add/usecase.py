from .request import AddParticipantRequest
from .response import AddParticipantResponse

from core.dependencies import get_participant_repository, get_chat_repository
from fastapi import HTTPException


class AddParticipantUsecase:
    async def __call__(self, request: AddParticipantRequest) -> AddParticipantResponse:
        chat = await get_chat_repository().get_by_id(id_=request.chat_id)
        if chat.user_id != request.user_id:
            raise HTTPException(status_code=404, detail="Can't add participant to other user's chat")
        await get_participant_repository().create(user_id=request.participant_id, chat_id=request.chat_id, added_by_id=request.user_id)
        return AddParticipantResponse(success=True)
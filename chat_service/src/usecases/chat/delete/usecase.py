from fastapi import HTTPException
from .request import DeleteChatRequest
from .response import DeleteChatResponse

from core.dependencies import get_chat_repository, get_participant_repository
from sdk.enums.user_type import UserType
import uuid

class DeleteChatUsecase:
    async def __call__(self, request: DeleteChatRequest) -> DeleteChatResponse:
        participant = await get_participant_repository().get_by_filter(user_id=uuid.UUID(request.user_id), chat_id=uuid.UUID(request.chat_id))
       
        if not participant:
            raise HTTPException(status_code=404, detail="Participant not found")

        if participant.user_type == UserType.USER or participant.user_type == UserType.ADMIN or str(participant.user_id) != str(request.user_id):
            raise HTTPException(status_code=404, detail="Can't delete chat")

        await get_chat_repository().delete(id_=request.chat_id)
        return DeleteChatResponse(success=True)
from .request import DeleteParticipantRequest
from .response import DeleteParticipantResponse
from fastapi import HTTPException

from core.dependencies import get_participant_repository

class DeleteParticipantUsecase:
    async def __call__(self, request: DeleteParticipantRequest) -> DeleteParticipantResponse:
        count_participants = await get_participant_repository().get_all_by_filter(chat_id=request.chat_id)
        if len(count_participants) == 1:
            raise HTTPException(status_code=404, detail="Can't delete participant")
        await get_participant_repository().delete(user_id=request.participant_id, chat_id=request.chat_id)
        return DeleteParticipantResponse(success=True)
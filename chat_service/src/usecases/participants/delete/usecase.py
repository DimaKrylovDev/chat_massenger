from .request import DeleteParticipantRequest
from .response import DeleteParticipantResponse
from fastapi import HTTPException

from core.dependencies import get_participant_repository
from sdk.enums.user_type import UserType

import uuid

class DeleteParticipantUsecase:
    async def __call__(self, request: DeleteParticipantRequest) -> DeleteParticipantResponse:
        participants = await get_participant_repository().get_all_by_filter(chat_id=request.chat_id)

        is_present = any(str(p.user_id) == str(request.user_id) for p in participants)

        if not is_present:
            raise HTTPException(status_code=404, detail="User not in chat")

        user = await get_participant_repository().get_by_filter(user_id=uuid.UUID(request.user_id), chat_id=request.chat_id)
        
        if user.user_type != UserType.OWNER:
            raise HTTPException(status_code=404, detail="Can't delete OWNER from chat")

        is_exist = await get_participant_repository().get_by_filter(user_id=uuid.UUID(request.participant_id), chat_id=request.chat_id)

        if not is_exist:
            raise HTTPException(status_code=404, detail="Participant not found")
        
        count_participants = await get_participant_repository().get_all_by_filter(chat_id=request.chat_id)

        if len(count_participants) == 1:
            raise HTTPException(status_code=404, detail="Can't delete yourself from chat")

        await get_participant_repository().delete_by_filter(user_id=uuid.UUID(request.participant_id), chat_id=uuid.UUID(request.chat_id))
        return DeleteParticipantResponse(success=True)
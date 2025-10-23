from .request import AddParticipantRequest
from .response import AddParticipantResponse

from core.dependencies import get_participant_repository
from fastapi import HTTPException
from sdk.enums.user_type import UserType

class AddParticipantUsecase:
    async def __call__(self, request: AddParticipantRequest) -> AddParticipantResponse:
        participants = await get_participant_repository().get_all_by_filter(chat_id=request.chat_id)
        
        is_present = any(p.user_id == request.user_id for p in participants)

        if not is_present:
            raise HTTPException(status_code=403, detail="User is not a participant of this chat")

        user = await get_participant_repository().get_by_filter(user_id=request.user_id, chat_id=request.chat_id)
        
        if user.user_type not in [UserType.OWNER, UserType.ADMIN]:
            raise HTTPException(status_code=403, detail="Insufficient permissions to add participants")
        
        if request.user_type == UserType.OWNER:
            raise HTTPException(status_code=400, detail="Cannot add OWNER type participant")

        existing_participant = await get_participant_repository().get_by_filter(
            user_id=request.participant_id, 
            chat_id=request.chat_id
        )
        
        if existing_participant:
            raise HTTPException(status_code=400, detail="Participant already exists in this chat")

        await get_participant_repository().create(
            user_id=request.participant_id, 
            chat_id=request.chat_id, 
            user_type=request.user_type
        )
        
        return AddParticipantResponse(success=True)
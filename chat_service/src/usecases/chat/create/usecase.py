from .request import CreateChatRequest
from .response import CreateChatResponse

from core.dependencies import get_chat_repository, get_participant_repository
from sdk.enums.user_type import UserType
import uuid 

class CreateChatUsecase:
    async def __call__(self, request: CreateChatRequest) -> CreateChatResponse:
        chat = await get_chat_repository().create(
            id=uuid.uuid4(),
            user_id=request.user_id,
            chat_name=request.chat_name,
            description=request.description,
        )

        await get_participant_repository().create(
            user_id=request.user_id,
            chat_id=chat.id,
            user_type=UserType.OWNER,
        )

        return CreateChatResponse(chat_id=str(chat.id), message="Chat created successfully", success=True)
        

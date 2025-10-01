from .request import CreateChatRequest
from .response import CreateChatResponse

from core.dependencies import get_chat_repository

class CreateChatUsecase:
    async def __call__(self, request: CreateChatRequest) -> CreateChatResponse:
        chat = await get_chat_repository().create(
            user_id=request.user_id,
            chat_name=request.chat_name,
            description=request.description,
        )
        return CreateChatResponse(chat_id=str(chat.id), message="Chat created successfully", success=True)
        

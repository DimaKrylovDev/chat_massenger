from .base import BaseRepository
from models.chat import Chat
from schemas.chat import Chat as ChatSchema
class ChatRepository(BaseRepository):
    model = Chat    
    model_schema = ChatSchema

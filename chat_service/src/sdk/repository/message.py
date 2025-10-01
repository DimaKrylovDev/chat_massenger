from .base import BaseRepository
from models.message import Message
from schemas.message import Message as MessageSchema

class MessageRepository(BaseRepository):
    model = Message
    model_schema = MessageSchema
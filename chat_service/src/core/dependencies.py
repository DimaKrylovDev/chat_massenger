from sdk.repository.chat import ChatRepository
from sdk.repository.message import MessageRepository
from sdk.repository.participants import ParticipantsRepository

def get_chat_repository():
    return ChatRepository()

def get_message_repository():
    return MessageRepository()

def get_participant_repository():
    return ParticipantsRepository()
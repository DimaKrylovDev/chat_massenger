"""
Утилиты для преобразования между Pydantic моделями и protobuf объектами
"""
from typing import List
from generated import chat_pb2
from schemas.chat import Chat as PydanticChat
from schemas.message import Message as PydanticMessage
from schemas.participant import Participant as PydanticParticipant


def pydantic_chat_to_proto(chat: PydanticChat) -> chat_pb2.Chat:
    """Преобразование Pydantic Chat в protobuf Chat"""
    proto_chat = chat_pb2.Chat()
    proto_chat.id = str(chat.id)
    proto_chat.name = chat.chat_name 
    proto_chat.description = chat.description
    proto_chat.created_at = chat.created_at.isoformat()

    return proto_chat


def pydantic_message_to_proto(message: PydanticMessage) -> chat_pb2.Message:
    proto_message = chat_pb2.Message()
    proto_message.id = str(message.id)
    proto_message.chat_id = str(message.chat_id)
    proto_message.user_id = str(message.user_id)
    proto_message.content = str(message.content)
    proto_message.message_type = str(message.message_type)
    proto_message.created_at = message.created_at.isoformat()
    
    return proto_message

def pydantic_participant_to_proto(participant: PydanticParticipant) -> chat_pb2.Participant:
    proto_participant = chat_pb2.Participant()
    proto_participant.user_id = str(participant.user_id)
    proto_participant.chat_id = str(participant.chat_id)
    
    return proto_participant
    
def pydantic_participants_to_proto(participants: List[PydanticParticipant]) -> List[chat_pb2.Participant]:
    return [pydantic_participant_to_proto(participant) for participant in participants]

def pydantic_chats_to_proto(chats: List[PydanticChat]) -> List[chat_pb2.Chat]:
    return [pydantic_chat_to_proto(chat) for chat in chats]

def pydantic_messages_to_proto(messages: List[PydanticMessage]) -> List[chat_pb2.Message]:
    return [pydantic_message_to_proto(message) for message in messages]

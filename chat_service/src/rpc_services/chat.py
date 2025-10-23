import grpc 
from generated import chat_pb2, chat_pb2_grpc
from usecases.chat.create.usecase import CreateChatUsecase
from usecases.chat.get.usecase import GetUserChatsUsecase
from usecases.message.send.usecase import SendMessageUsecase
from usecases.message.get.usecase import GetMessagesUsecase

from usecases.chat.create.request import CreateChatRequest
from usecases.chat.get.request import GetUserChatsRequest
from usecases.message.send.request import SendMessageRequest
from usecases.message.get.request import GetMessagesRequest
from usecases.participants.add.request import AddParticipantRequest
from usecases.participants.delete.request import DeleteParticipantRequest
from usecases.participants.add.usecase import AddParticipantUsecase
from usecases.participants.delete.usecase import DeleteParticipantUsecase
from usecases.message.delete.request import DeleteMessageRequest
from usecases.message.delete.usecase import DeleteMessageUsecase
from usecases.chat.delete.usecase import DeleteChatUsecase
from usecases.chat.delete.request import DeleteChatRequest
from usecases.participants.get.usecase import GetChatParticipantsUsecase
from usecases.participants.get.request import GetChatParticipantsRequest
from utils.proto_converter import pydantic_chats_to_proto, pydantic_messages_to_proto, pydantic_participants_to_proto


class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.create_chat_uc = CreateChatUsecase()
        self.get_user_chats_uc = GetUserChatsUsecase()
        self.send_message_uc = SendMessageUsecase()
        self.get_messages_uc = GetMessagesUsecase()
        self.add_participant_uc = AddParticipantUsecase()
        self.delete_participant_uc = DeleteParticipantUsecase()
        self.delete_message_uc = DeleteMessageUsecase()
        self.delete_chat_uc = DeleteChatUsecase()
        self.get_chat_participants_uc = GetChatParticipantsUsecase()

    async def CreateChat(self, request: chat_pb2.CreateChatRequest, context: grpc.ServicerContext) -> chat_pb2.CreateChatResponse:
        request = CreateChatRequest(
            user_id=request.user_id,
            chat_name=request.chat_name,
            description=request.description,
        )
        result = await self.create_chat_uc(request=request)
        return chat_pb2.CreateChatResponse(
            chat_id=result.chat_id,
            message=result.message,
            success=result.success)

    async def GetUserChats(self, request: chat_pb2.GetUserChatsRequest, context: grpc.ServicerContext) -> chat_pb2.GetUserChatsResponse:
        try:
            request = GetUserChatsRequest(
                user_id=request.user_id,
            )
            result = await self.get_user_chats_uc(request=request)

            proto_chats = pydantic_chats_to_proto(result.chats)

            return chat_pb2.GetUserChatsResponse(
                chats=proto_chats,
                total_count=result.total_count)
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e)) 

    async def SendMessage(self, request: chat_pb2.SendMessageRequest, context: grpc.ServicerContext) -> chat_pb2.SendMessageResponse:
        try:
            request = SendMessageRequest(
                user_id=request.user_id,
                chat_id=request.chat_id,
                content=request.content,
                message_type=request.message_type
            )
            result = await self.send_message_uc(request=request)

            return chat_pb2.SendMessageResponse(
                message_id=str(result.message_id),
                message=str(result.message),
                success=bool(result.success)
            )
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def GetMessages(self, request: chat_pb2.GetMessagesRequest, context: grpc.ServicerContext) -> chat_pb2.GetMessagesResponse:
        try:
            request = GetMessagesRequest(
                user_id=request.user_id,
                chat_id=request.chat_id,
            )
            result = await self.get_messages_uc(request=request)

            proto_messages = pydantic_messages_to_proto(result.messages)

            return chat_pb2.GetMessagesResponse(
                messages=proto_messages,
                total_count=result.total_count)
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def AddParticipant(self, request: chat_pb2.AddParticipantRequest, context: grpc.ServicerContext) -> chat_pb2.AddParticipantResponse:
        try:
            # Конвертируем строки в UUID
            import uuid
            from sdk.enums.user_type import UserType

            user_type_mapping = {
                0: UserType.USER,
                1: UserType.ADMIN, 
                2: UserType.OWNER
            }
            
            add_request = AddParticipantRequest(
                user_id=uuid.UUID(request.user_id),
                participant_id=uuid.UUID(request.participant_id),
                chat_id=uuid.UUID(request.chat_id),
                user_type=user_type_mapping[request.user_type]
            )
            result = await self.add_participant_uc(request=add_request)
            return chat_pb2.AddParticipantResponse(success=result.success)
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def DeleteParticipant(self, request: chat_pb2.DeleteParticipantRequest, context: grpc.ServicerContext) -> chat_pb2.DeleteParticipantResponse:
        try:
            request = DeleteParticipantRequest(
            user_id=request.user_id,
            participant_id=request.participant_id,
            chat_id=request.chat_id
            )
            result = await self.delete_participant_uc(request=request)
            return chat_pb2.DeleteParticipantResponse(success=result.success)
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def GetChatParticipants(self, request: chat_pb2.GetChatParticipantsRequest, context: grpc.ServicerContext) -> chat_pb2.GetChatParticipantsResponse:
        try:
            request = GetChatParticipantsRequest(
            user_id=request.user_id,
            chat_id=request.chat_id
            )
            result = await self.get_chat_participants_uc(request=request)

            proto_participants = pydantic_participants_to_proto(result.participants)

            return chat_pb2.GetChatParticipantsResponse(participants=proto_participants, total_count=result.total_count)
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def DeleteMessage(self, request: chat_pb2.DeleteMessageRequest, context: grpc.ServicerContext) -> chat_pb2.DeleteMessageResponse:
        try:
            request = DeleteMessageRequest(
            user_id=request.user_id,
            chat_id=request.chat_id,
            message_id=request.message_id
            )
            result = await self.delete_message_uc(request=request)
            return chat_pb2.DeleteMessageResponse(success=result.success)
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def DeleteChat(self, request: chat_pb2.DeleteChatRequest, context: grpc.ServicerContext) -> chat_pb2.DeleteChatResponse:
        try:
            request = DeleteChatRequest(
            user_id=request.user_id,
            chat_id=request.chat_id
            )
            result = await self.delete_chat_uc(request=request)
            return chat_pb2.DeleteChatResponse(success=result.success)
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e))
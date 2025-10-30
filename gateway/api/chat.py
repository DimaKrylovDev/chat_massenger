from fastapi import APIRouter, Depends, Security, HTTPException
from security.auth import JWTGetter
from config.settings import settings
from clients.async_grpc_client import get_clients, AsyncGrpcClients
from generated import chat_pb2
from schemas.chat.chat import (
    CreateChatRequest, DeleteChatRequest, GetUserChatsRequest,
    CreateChatResponse, GetUserChatsResponse, DeleteChatResponse)
from schemas.auth.token import Token

router = APIRouter()

get_token = JWTGetter(settings.EE_SECRET_KEY)

@router.post('/create', response_model=CreateChatResponse)
async def create_chat(request: CreateChatRequest, token: Token = Security(get_token), client: AsyncGrpcClients = Depends(get_clients)):
    user_id = token.user_id
    if not user_id:
        raise HTTPException(status_code=401, detail='Unauthorized')

    request = chat_pb2.CreateChatRequest(user_id=user_id, chat_name=request.chat_name, description=request.description)
    response = await client.chat_stub.CreateChat(request)
    result = CreateChatResponse(chat_id=response.chat_id, message=response.message, success=response.success)
    return result

@router.post('/get', response_model=GetUserChatsResponse)
async def get_user_chats(request: GetUserChatsRequest, token: Token = Security(get_token), client: AsyncGrpcClients = Depends(get_clients)):   
    user_id = token.user_id 
    if not user_id:
        raise HTTPException(status_code=401, detail='Unauthorized')

    request = chat_pb2.GetUserChatsRequest(user_id=user_id)
    response = await client.chat_stub.GetUserChats(request)
    result = GetUserChatsResponse(chats=response.chats, total_count=response.total_count)
    return result

@router('/delete', response_model=DeleteChatResponse)
async def delete_chat(request: DeleteChatRequest, token: Token = Security(get_token), client: AsyncGrpcClients = Depends(get_clients)):
    user_id = token.user_id
    
    if not user_id:
        raise HTTPException(status_code=401, detail='Unauthorized')
    
    request = chat_pb2.DeleteChatRequest(user_id = user_id, chat_id = request.chat_id)
    response = await client.chat_stub.DeleteChat(request)
    result = DeleteChatResponse(success=response.success)
    return result
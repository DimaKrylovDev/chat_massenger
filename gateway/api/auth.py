from fastapi import APIRouter, Depends, Security, HTTPException
from security.auth import JWTGetter
from config.settings import settings
from clients.async_grpc_client import get_clients, AsyncGrpcClients
from generated import auth_pb2
from schemas.auth.requests import SignUpRequest, LoginRequest
from schemas.auth.responses import (
    SignUpResponse, LoginResponse, 
    RefreshResponse, LogoutResponse, 
    ValidateResponse)
from schemas.auth.token import Token

router = APIRouter()

get_token = JWTGetter(settings.EE_SECRET_KEY)

@router.post("/validate")
async def validate_token(token: Token = Security(get_token), client: AsyncGrpcClients = Depends(get_clients)):
    request = auth_pb2.ValidateTokenRequest(access_token=token.jwt_string)
    response = await client.auth_stub.ValidateToken(request)
    result = ValidateResponse(valid=response.valid, user_id=response.user_id, error_message=response.error_message)
    return result.valid 

@router.post("/signup")
async def signup(request: SignUpRequest, client: AsyncGrpcClients = Depends(get_clients)):
    request = auth_pb2.SignUpRequest(username=request.username, email=request.email, password=request.password, bio=request.bio)
    response = await client.auth_stub.SignUp(request)
    result = SignUpResponse(access_token=response.access_token, refresh_token=response.refresh_token)
    return result

@router.post("/login")
async def login(request: LoginRequest, client: AsyncGrpcClients = Depends(get_clients)):
    request = auth_pb2.LoginRequest(email=request.email, password=request.password)
    response = await client.auth_stub.Login(request)
    result = LoginResponse(access_token=response.access_token, refresh_token=response.refresh_token)
    return result

@router.post("/refresh")
async def refresh(token: Token = Security(get_token), client: AsyncGrpcClients = Depends(get_clients)):
    session_id = token.session_id
    
    if not session_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    request = auth_pb2.RefreshRequest(session_id=str(session_id))
    response = await client.auth_stub.RefreshToken(request)
    result = RefreshResponse(access_token=response.access_token)
    return result

@router.post("/logout")
async def logout(token: Token = Security(get_token), client: AsyncGrpcClients = Depends(get_clients)):
    session_id = token.session_id
    if not session_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    request = auth_pb2.LogoutRequest(session_id=str(session_id))
    response = await client.auth_stub.Logout(request)
    result = LogoutResponse(message=response.message)
    return result


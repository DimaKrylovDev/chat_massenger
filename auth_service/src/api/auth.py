from fastapi import APIRouter, Depends

from generated import auth_pb2, auth_pb2_grpc
from core.security import JWTGetter
from core.settings import settings
from schemas.token import Token
from usecases.login.request import LoginRequest
from usecases.login.response import LoginResponse
from usecases.logout.response import LogoutResponse
from usecases.signup.request import SignUpRequest
from usecases.signup.response import SignUpResponse
from usecases.refresh.response import RefreshResponse

jwt_getter = JWTGetter(settings.EE_SECRET_KEY)

router = APIRouter(prefix="/auth")

tags_metadata = [
    {
        "name": "Auth",
        "description": "User auth methods",
    }
]


@router.post("/signup", tags=["Auth"])
async def signup(request: SignUpRequest):
    async with settings.GRPC_CHANNEL as channel:
        stub = auth_pb2_grpc.AuthServiceStub(channel)
        response = await stub.SignUp(auth_pb2.SignUpRequest(username=request.username, 
                                                            email=request.email, 
                                                            password=request.password, 
                                                            bio=request.bio))
        return SignUpResponse(
            access_token=response.access_token,
            refresh_token=response.refresh_token,
            token_type=response.token_type
        )

@router.post("/login", tags=["Auth"])
async def login(request: LoginRequest):
    async with settings.GRPC_CHANNEL as channel:
        stub = auth_pb2_grpc.AuthServiceStub(channel)
        response = await stub.Login(auth_pb2.LoginRequest(email=request.email, 
                                                          password=request.password))
        return LoginResponse(
            access_token=response.access_token,
            refresh_token=response.refresh_token,
            token_type=response.token_type
        )

@router.post("/refresh", tags=["Auth"])
async def refresh(token: Token = Depends(jwt_getter)):
    async with settings.GRPC_CHANNEL as channel:
        stub = auth_pb2_grpc.AuthServiceStub(channel)
        token = auth_pb2.Token(
            jwt_string=token.jwt_string,
            user_id=token.user_id or "",
            session_id=token.session_id or "",
            exp=int(token.exp)
        )
        response = await stub.RefreshToken(auth_pb2.RefreshRequest(token=token))
        return RefreshResponse(
            access_token=response.access_token,
            token_type=response.token_type
        )

@router.post("/logout", tags=["Auth"])
async def logout(token: Token = Depends(jwt_getter)):
    async with settings.GRPC_CHANNEL as channel:
        stub = auth_pb2_grpc.AuthServiceStub(channel)
        token = auth_pb2.Token(
            jwt_string=token.jwt_string,
            user_id=token.user_id or "",
            session_id=token.session_id or "",
            exp=int(token.exp)
        )
        response = await stub.Logout(auth_pb2.LogoutRequest(token=token))

        return LogoutResponse(message=response.message)

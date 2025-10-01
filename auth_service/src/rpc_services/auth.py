import asyncio
from passlib import context
from generated import auth_pb2, auth_pb2_grpc
import grpc

from usecases.signup.usecase import SignUpUsecase
from usecases.login.usecase import LoginUsecase
from usecases.refresh.usecase import RefreshUsecase
from usecases.logout.usecase import LogoutUsecase

from usecases.signup.request import SignUpRequest
from usecases.login.request import LoginRequest
from usecases.refresh.request import RefreshRequest
from usecases.logout.request import LogoutRequest
from usecases.validate.usecase import ValidateTokenUsecase
from usecases.validate.request import ValidateTokenRequest

from schemas.token import Token


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def __init__(self):
        self.signup_uc = SignUpUsecase()
        self.login_uc = LoginUsecase()
        self.refresh_uc = RefreshUsecase()
        self.logout_uc = LogoutUsecase()
        self.validate_token_uc = ValidateTokenUsecase()

    async def SignUp(self, request: auth_pb2.SignUpRequest, context: grpc.ServicerContext) -> auth_pb2.SignUpResponse:
        try:
            request = SignUpRequest(
                username=str(request.username),
                email=str(request.email),
                password=str(request.password),
                bio=str(request.bio)
            )
            result = await self.signup_uc(request=request)
            return auth_pb2.SignUpResponse(
                access_token=result.access_token or "",
                refresh_token=result.refresh_token or "",
                token_type="Bearer"
            )
        except ValueError as e:
            if "User already exists" in str(e):
                await context.abort(grpc.StatusCode.ALREADY_EXISTS, str(e))
            elif "Username already exists" in str(e):
                await context.abort(grpc.StatusCode.ALREADY_EXISTS, str(e))
            elif "Failed to create user" in str(e):
                await context.abort(grpc.StatusCode.INTERNAL, str(e))
            else:
                await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))

    async def Login(self, request: auth_pb2.LoginRequest, context: grpc.ServicerContext) -> auth_pb2.LoginResponse:
        try:
            request = LoginRequest(
                email=request.email,
                password=request.password
            )
            result = await self.login_uc(request=request)
            return auth_pb2.LoginResponse(
                access_token=result.access_token,
                refresh_token=result.refresh_token,
                token_type="Bearer"
            )
        except ValueError as e:
            if "Invalid credentials" in str(e):
                await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
            elif "Invalid password" in str(e):
                await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
            else:
                await context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def RefreshToken(self, request: auth_pb2.RefreshRequest, context: grpc.ServicerContext) -> auth_pb2.RefreshResponse:
        try:
            request = RefreshRequest(
                session_id=request.session_id
            )
            result = await self.refresh_uc(request=request)
            return auth_pb2.RefreshResponse(
                access_token=str(result.access_token),
                token_type="Bearer"
            )
        except ValueError as e:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))

    async def Logout(self, request: auth_pb2.LogoutRequest, context: grpc.ServicerContext) -> auth_pb2.LogoutResponse:
        try:
            request = LogoutRequest(
                session_id=request.session_id
            )
            result = await self.logout_uc(request=request)
            return auth_pb2.LogoutResponse(message=result.message) 
        except ValueError as e:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))

    async def ValidateToken(self, request: auth_pb2.ValidateTokenRequest, context: grpc.ServicerContext) -> auth_pb2.ValidateTokenResponse:
        try:
            request = ValidateTokenRequest(
                access_token=request.access_token
            )
            result = await self.validate_token_uc(request=request)
            return auth_pb2.ValidateTokenResponse(valid=result.valid, user_id=result.user_id, error_message=result.error_message)
        except ValueError as e: 
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
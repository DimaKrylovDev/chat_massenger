from passlib import context
from generated import auth_pb2, auth_pb2_grpc
from usecases.base import AuthBaseUsecase
from core.dependencies import get_auth_repository, get_session_repository
import grpc
import datetime
from concurrent import futures


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def __init__(self):
        self.user_repo = get_auth_repository()
        self.session_repo = get_session_repository()
        self.AuthUc = AuthBaseUsecase()

    async def SignUp(self, request: auth_pb2.SignUpRequest, context: grpc.ServicerContext) -> auth_pb2.SignUpResponse:
        existing_user = await self.user_repo.get_by_email(request.email)
        if existing_user:
           await context.abort(grpc.StatusCode.ALREADY_EXISTS, "User already exists")
        
        existing_username = await self.user_repo.get_by_username(request.username)
        if existing_username:
           await context.abort(grpc.StatusCode.ALREADY_EXISTS, "Username already exists")

        hashed_password = await self.AuthUc.hash_password(request.password)
        
        user = await self.AuthUc.create_user(
            username=request.username,
            email=request.email,
            hashed_password=hashed_password,
            bio=request.bio,
        )

        print(user)

        if not user:
            await context.abort(grpc.StatusCode.INTERNAL, "Failed to create user")
        
        session = await self.AuthUc.create_session(user_id=user.id, last_active_at=datetime.datetime.now())

        access_token = await self.AuthUc.create_access_token(str(user.id))
        refresh_token = await self.AuthUc.create_refresh_token(str(session.id))

        return auth_pb2.SignUpResponse(
            access_token=access_token, 
            refresh_token=refresh_token)

    async def Login(self, request: auth_pb2.LoginRequest, context: grpc.ServicerContext) -> auth_pb2.LoginResponse:
        user = await self.AuthUc.find_user_by_email(request.email)
        if not user:
            await context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

        if not await self.AuthUc.verify_password(password=request.password, hashed_password=user.hashed_password):
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid password")

        access_token = await self.AuthUc.create_access_token(str(user.id))

        last_active_at = datetime.datetime.now()
        session = await self.AuthUc.create_session(user_id=user.id, last_active_at=last_active_at)
        refresh_token = await self.AuthUc.create_refresh_token(str(session.id))

        return auth_pb2.LoginResponse(access_token=access_token, refresh_token=refresh_token)

    async def RefreshToken(self, request: auth_pb2.RefreshRequest, context: grpc.ServicerContext) -> auth_pb2.RefreshResponse:
        session = await self.AuthUc.find_session_by_id(request.token.session_id)
        if not session:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Session not found")

        await self.AuthUc.update_session(request.token.session_id, last_active_at=datetime.datetime.now())

        access_token = await self.AuthUc.create_access_token(str(session.user_id))  
        refresh_token = await self.AuthUc.create_refresh_token(str(session.id))

        return auth_pb2.RefreshResponse(access_token=access_token, refresh_token=refresh_token)

    async def Logout(self, request: auth_pb2.LogoutRequest, context: grpc.ServicerContext) -> auth_pb2.LogoutResponse:
        session = await self.AuthUc.find_session_by_token(request.token.session_id)
        if not session:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Session not found")

        data = dict(
            is_active=False,
            last_active_at=datetime.datetime.now()
        )

        await self.AuthUc.update_session(str(session.id), **data)

        return auth_pb2.LogoutResponse(message="Logged out successfully")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("server started")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()   
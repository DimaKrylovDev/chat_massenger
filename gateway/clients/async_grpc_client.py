import grpc.aio
from generated import auth_pb2_grpc
from generated import chat_pb2_grpc

from config.settings import settings

class AsyncGrpcClients:
    def __init__(self):
        self._auth_channel: [grpc.aio.Channel] = None
        self._chat_channel: [grpc.aio.Channel] = None

        self._auth_stub: [auth_pb2_grpc.AuthServiceStub] = None
        self._chat_stub: [chat_pb2_grpc.ChatServiceStub] = None

    
    async def init_auth_channel(self, host: str, port: int) -> grpc.aio.Channel:
        self._auth_channel = grpc.aio.insecure_channel(f"{host}:{port}")
        self._auth_stub = auth_pb2_grpc.AuthServiceStub(self._auth_channel)

    async def init_chat_channel(self, host: str, port: int) -> grpc.aio.Channel:
        self._chat_channel = grpc.aio.insecure_channel(f"{host}:{port}")
        self._chat_stub = chat_pb2_grpc.ChatServiceStub(self._chat_channel)

    @property
    def auth_stub(self) -> auth_pb2_grpc.AuthServiceStub:
        if not self._auth_stub:
            raise ValueError("Auth stub not initialized")
        return self._auth_stub

    @property
    def chat_stub(self) -> chat_pb2_grpc.ChatServiceStub:
        if not self._chat_stub:
            raise ValueError("Chat stub not initialized")
        return self._chat_stub

    async def close(self):
        await self._auth_channel.close()
        await self._chat_channel.close()

_clients = AsyncGrpcClients()

def get_clients() -> AsyncGrpcClients:
    return _clients
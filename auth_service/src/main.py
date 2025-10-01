import asyncio
import grpc

from generated import auth_pb2_grpc
from rpc_services.auth import AuthService

async def serve():
    server = grpc.aio.server()
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port("[::]:50050")
    await server.start()
    print("server started on port 50050")
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())
import asyncio
import grpc

from generated import chat_pb2_grpc
from rpc_services.chat import ChatService

async def serve():
    server = grpc.aio.server()
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    print("server started on port 50051")
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())
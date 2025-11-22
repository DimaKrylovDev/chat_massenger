from fastapi import WebSocket 
from typing import List, Dict, Set
import asyncio
from uuid import UUID
from managers.pubsub_manager import RedisPubSubManager

class WebSocketManager():
    def __init__(self):
        self.handlers = {}
        self.active_connections: Set[WebSocket] = set()
        self.chat_connections: dict = {}
        self.user_connections: dict = {}
        self.pubsub_client = RedisPubSubManager()

    async def handler(self, message_type):
        def decorator(func):
            self.handlers[message_type] = func
            return func 

        return decorator
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept() 
        self.active_connections.add(websocket)
    
    async def add_user_socket_connection(self, websocket: WebSocket, user_id: UUID):
        if user_id not in self.user_connections:
            self.user_connections[user_id] = set()
        self.user_connections[user_id].add(websocket)

    async def disconnect(self, websocket: WebSocket, user_id: UUID):
        self.active_connections.discard(websocket)

        if user_id in self.user_connections:
            self.user_connections[user_id].discard(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]

    async def add_user_to_chat(self, websocket: WebSocket, chat_id: UUID):
        if chat_id not in self.chat_connections:
            self.chat_connections[chat_id] = set()
        
        if websocket in self.chat_connections[chat_id]:
            return f"User already in chat"
            
        self.chat_connections[chat_id].add(websocket)

        if len(self.chat_connections[chat_id]) == 1:
            await self.pubsub_client.connect()
            pubsub_sub = await self.pubsub_client.subcribe(chat_id=chat_id)
            asyncio.create_task(self._read_pubsub_data(chat_id=chat_id, pubsub_subcriber=pubsub_sub))

    async def remove_user_from_chat(self, websocket: WebSocket,  chat_id: UUID):
            try:
                if chat_id in self.chat_connections:
                    self.chat_connections[chat_id].discard(websocket)

                    if not self.chat_connections[chat_id]:
                        del self.chat_connections[chat_id]
                        await self.pubsub_client.unsubcribe(chat_id=chat_id)

            except Exception as e:
                raise f"Exception in leave_chat: {e}"
        

    async def broadcast_to_chat(self, chat_id: UUID, message: dict | str):
        if chat_id not in self.chat_connections:
            raise "Failed to broadcast chat: chat_id not in list"
        
        self.pubsub_client.publish(message=message, chat_id=chat_id)

    async def _read_pubsub_data(self, pubsub_subcriber, chat_id: UUID):
        try:
            async for message in pubsub_subcriber.listen():
                if message["type"] != "message":
                    continue
     
                channel = message["channel"].decode("utf-8")
                data = message["data"].decode("utf-8")
                if channel == str(chat_id):
                    sockets = self.chat_connections.get(channel, set()).copy()
                    if sockets:
                        for socket in list(sockets):
                            try:
                                socket.send_text(data)
                            except Exception as e:
                                raise f"Failed send to socket: {e}"
        except Exception as e:
            raise f"Pubsub reader error: {e}"

    async def send_error(self, message: str, websocket: WebSocket):
        return websocket.send_json({"status": "error", "message": message})
    
manager = WebSocketManager()


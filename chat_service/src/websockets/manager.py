from fastapi import WebSocket 
from typing import List, Dict, Set

class WebSocketManager():
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.chat_connections: Dict(str, Dict(str, WebSocket)) = {} 
        self.user_connections: Dict(str, List[WebSocket]) = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept
        if user_id not in self.user_connections.keys():
            self.user_connections[user_id] = [] 

        self.user_connections[user_id] = websocket
        self.active_connections.add(websocket)

        #TODO

    async def disconnect(self, websocket: WebSocket, user_id: int ):
        self.active_connections.discard(websocket)
        
        if user_id in self.chat_connections:
            if websocket in self.user_connections[user_id]
            self.user_connections[user_id].remove(websocket)

            if not self.user_connections[user_id]:
                del self.user_connections[user_id] 

        for chat_id in list(self.chat_connections.keys()):
            if user_id in self.chat_connections[user_id]:
                del self.chat_connections[chat_id][user_id]

            if not self.chat_connections[chat_id]:
                del self.chat_connections[chat_id]

    async def join_chat(self, websocket: WebSocket, user_id: int, chat_id: int):
        if chat_id not in self.chat_connections:
            self.chat_connections[chat_id] = {}

        if not self.chat_connections[chat_id][user_id]:
            self.chat_connections[chat_id][user_id] = websocket

        #TODO notify

    async def leave_chat(self, websocket: WebSocket, user_id: int, chat_id: int):
        if chat_id in self.chat_connections[chat_id] and user_id in self.chat_connections[chat_id][user_id]:
            del self.chat_connections[chat_id][user_id]

        #TODO notify 

    async def send_to_user(self, websocket: WebSocket, user_id: int, message: str):
        if user_id in self.user_connections:
            try:
                websocket.send_text(message)
            except:
                await self.disconnect(websocket, user_id)

    async def broadcast_to_chat(self, chat_id: int, message: str):
        for client in self.active_connections:
            await client.send_text(message)

manager = WebSocketManager()


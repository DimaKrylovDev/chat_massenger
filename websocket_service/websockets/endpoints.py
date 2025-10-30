from fastapi import APIRouter, WebSocket
from uuid import UUID
from fastapi_limiter.depends import WebSocketRateLimiter

from manager import manager  
router = APIRouter() 

@router.websocket('/ws/chat')
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: UUID
):
    await manager.connect(websocket, user_id)
    ratelimiter = WebSocketRateLimiter(times=50, seconds=10, callback="Too many requests")d
    pass
 


from fastapi import WebSocket, Depends
import redis.asyncio as aioredis
from uuid import UUID
from managers.pubsub_manager import RedisPubSubManager
from managers.rabbitmq_manager import RabbitMQManager
from managers.websocket_manager import WebSocketManager
from config.dependencies import get_rabbitq_manager, get_websocket_manager,get_redis_manager
from config.settings import settings
from schemas.messages import SReceiveMessage, SSendMessage
import json
import datetime

manager = WebSocketManager()

@manager.handler("new_message")
async def new_message(
    websocket: WebSocket,    
    incoming_message: dict,
    user_id: UUID,
    websocket_manager: WebSocketManager,
    redis_client: RedisPubSubManager,
    rabbitmq: RabbitMQManager
):
    message_schema = SReceiveMessage(**incoming_message)
    chat_id = str(message_schema.chat_id)

    send_message_schema = SSendMessage(
        chat_id = chat_id,
        user_id = user_id, 
        content = message_schema.content,
        created_at = datetime.datetime.now(),
        message_type = 'txt'
    )

    await websocket_manager.add_user_to_chat(websocket=websocket, chat_id=chat_id)
    system_msg = json.dumps({"type": "system", "event": "user_joined", "user_id": str(user_id)})
    await websocket_manager.broadcast_to_chat(chat_id=chat_id, message=system_msg)

    outgoing_message: dict = send_message_schema.model_dump_json()
    await websocket_manager.broadcast_to_chat(chat_id=chat_id, message=outgoing_message)

    await redis_client.publish(chat_id=chat_id, message=json.dumps(outgoing_message))

    outgoing_message = {
        "type": "new_message",
        "content": message_schema.content,
        "chat_id": chat_id,
        "user_id": user_id
    }

    await rabbitmq.publish(message_data=outgoing_message, routing_key=settings.routing_key_to_chat_service)

    await websocket_manager.broadcast_to_chat(chat_id=chat_id, message="new message")
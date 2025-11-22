from fastapi import APIRouter, WebSocket, Depends
from uuid import UUID
from config.dependencies import get_websocket_manager, get_redis_manager, get_rabbitq_manager

from managers.websocket_manager import WebSocketManager
from managers.rabbitmq_manager import RabbitMQManager
from managers.pubsub_manager import RedisPubSubManager

from fastapi.websockets import WebSocketDisconnect

from config.settings import settings

router = APIRouter() 

@router.websocket('/ws/chat')
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: UUID,
    websocket_manager: WebSocketManager = Depends(get_websocket_manager),
    rabbitmq_manager: RabbitMQManager = Depends(get_rabbitq_manager),
    redis_client: RedisPubSubManager = Depends(get_redis_manager)
):
    await websocket_manager.connect(websocket=websocket)
    
    await websocket_manager.add_user_socket_connection(websocket=websocket, user_id=user_id)

    rabbitmq_manager.consume(settings.queue_name_to_chat_service, routing_key=settings.routing_key_to_chat_service, callback=callback)

    #TODO start_consume from chat_service for data from postgresql and check if chat_exist

    try:
        while True:
            incoming_message = await websocket.receive_json()
            message_type = incoming_message.get("type")

            if not message_type:
                await websocket_manager.send_error(message="You should provide message type", websocket=websocket)
                continue

            handler = websocket_manager.handlers.get(message_type)

            if not handler:
                await websocket_manager.send_error(f"{message_type} not found", websocket=websocket)
                continue

            await handler(
                websocket=websocket,    
                incoming_message=incoming_message,
                user_id=user_id,
                websocket_manager=websocket_manager,
                redis_client=redis_client,
                rabbitmq=rabbitmq_manager
            )
    except WebSocketDisconnect as e:
        await websocket_manager.disconnect(websocket, user_id)

    except Exception as e:
        await websocket.close(code=1011, reason="Internal error")
        await websocket_manager.disconnect(websocket, user_id)
     
            




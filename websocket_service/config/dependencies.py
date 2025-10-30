from managers.rabbitmq_manager import RabbitMQManager
from managers.pubsub_manager import RedisPubSubManager
from managers.websocket_manager import WebSocketManager


websocket_manager = WebSocketManager()
rabbit_client = RabbitMQManager()
redis_client = RedisPubSubManager()

def get_rabbitq_manager():
    rabbit_client.ensure_connection()
    return rabbit_client

def get_redis_manager():
   return redis_client 

def get_websocket_manager():
    return websocket_manager


from aio_pika import ExchangeType, IncomingMessage
import aio_pika
from config.settings import settings
import json
from typing import Callable
import asyncio

class RabbitMQManager:
    def __init__(self):
        self.connection = None
        self.exchange = None
        self.channel = None
        self._is_connected = None 

    async def connect(self):
        self.connection = await aio_pika.connect_robust(host="rabbitmq")
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(name="chat_events", type=settings.exchanger)

        try:
            queue = await self.channel.get_queue(settings.queue_name_to_chat_service)
        except aio_pika.exceptions.ChannelNotFoundEntity:
            queue = await self.channel.declare_queue(settings.queue_name_to_chat_service, durable=True)

        self._is_connected = True

    async def ensure_connection(self):
        if not self._is_connected or self.connection.closed():
            await self.connect()
                
    async def publish(self, routing_key: str, message_data: str):
        await self.ensure_connection()

        try:
            message = aio_pika.Message(body=json.dumps(message_data).encode(), content_type="application/json")
            await self.exchange.publish(message=message, routing_key=routing_key)
        except aio_pika.exceptions.PublishError as e:
            raise f"Error with Publish: {e}"

    async def consume(self, queue_name: str, routing_key: str, callback: Callable):
        await self.ensure_connection()

        try: 
            queue = await self.channel.declare_queue(queue_name, durable=True)
            await queue.bind(exchange=settings.exchanger, routing_key=routing_key)
            await queue.consume(callback=callback)
        except Exception as  e:
            raise f"Exception with consume: {e}"

    async def start_consume(self, queue_name: str):
        asyncio.create_task(self.consume(queue_name))

    async def close(self):
        if self.connection:
            self.connection.close()
            self._is_connected = False
    

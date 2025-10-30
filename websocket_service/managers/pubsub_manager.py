import redis.asyncio as aioredis
from database.db import redis_pool

from uuid import UUID

class RedisPubSubManager:
    def __init__(self):
        self.pubsub = None
        self.redis_connection = None

    async def _get_redis_connection(self) -> aioredis.Redis:
        return aioredis.Redis(connection_pool=redis_pool)

    async def connect(self) -> aioredis.Redis:
        self.redis_connection = await self._get_redis_connection()
        self.pubsub = self.redis_connection.pubsub()

    async def publish(self, chat_id: UUID, message: str):
        await self.redis_connection.publish(str(chat_id), message) 

    async def subscribe(self, chat_id: UUID) -> aioredis.Redis:
        await self.pubsub.subscribe(str(chat_id))
        return self.pubsub

    async def unsubscribe(self, chat_id: UUID):
        await self.pubsub.unsubcribe(str(chat_id))

    async def disconnect(self):
        if self.pubsub:
            await self.pubsub.close()
        if self.redis_connection:
            await self.redis_connection.close()
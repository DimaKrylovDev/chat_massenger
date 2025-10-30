import redis.asyncio as aioredis
from config.settings import settings

def create_redis_pool():
    return aioredis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

redis_pool = create_redis_pool()


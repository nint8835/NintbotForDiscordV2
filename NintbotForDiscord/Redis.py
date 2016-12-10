from typing import Tuple
import aioredis
from discord import Server, Channel, User

from NintbotForDiscord.BasePlugin import BasePlugin
from . import Bot
from .Enums import RedisStorageScope


class RedisManager(object):

    def __init__(self, bot: "Bot.Bot", address: Tuple[str, int]):
        self._bot = bot  # type: Bot.Bot
        self._address = address  # type: Tuple[str, int]
        self.conn = None  # type: aioredis.Redis
        self._bot.EventManager.loop.create_task(self.connect())

    async def connect(self):
        self.conn = await aioredis.create_redis(self._address,
                                                loop=self._bot.EventManager.loop)

    def get_storage(self, obj=None):
        if obj is None:
            return RedisStorage(self.conn)
        else:
            if isinstance(obj, BasePlugin):
                return RedisStorage(self.conn, RedisStorageScope.PLUGIN, obj)
            elif isinstance(obj, Server):
                return RedisStorage(self.conn, RedisStorageScope.SERVER, obj)
            elif isinstance(obj, Channel):
                return RedisStorage(self.conn, RedisStorageScope.CHANNEL, obj)
            elif isinstance(obj, User):
                return RedisStorage(self.conn, RedisStorageScope.USER, obj)


class RedisStorage(object):

    def __init__(self, redis: aioredis.Redis, scope: RedisStorageScope=RedisStorageScope.GLOBAL, scope_obj=None):
        self.scope = scope
        self.object = scope_obj  # type: RedisStorageScope
        self.redis = redis  # type: aioredis.Redis

    def generate_key(self, key: str) -> str:
        if self.scope == RedisStorageScope.GLOBAL:
            return "GLOBAL:{}".format(key)
        elif self.scope == RedisStorageScope.PLUGIN:
            return "PLUGIN:{}:{}".format(self.object.PLUGIN_NAME.replace(" ", ""), key)
        else:
            return "{}:{}:{}".format(self.scope.name, self.object.id, key)

    async def delete(self, key):
        return await self.redis.delete(self.generate_key(key))

    async def set(self, key, value, expire: int=0):
        return await self.redis.set(self.generate_key(key),
                                    value,
                                    expire=expire)

    async def get(self, key):
        return await self.redis.get(self.generate_key(key))

    async def smembers(self, key):
        return await self.redis.smembers(self.generate_key(key))

    async def srem(self, key, value):
        return await self.redis.srem(self.generate_key(key), value)

    async def sadd(self, key, member, *members):
        return await self.redis.sadd(self.generate_key(key), member, *members)

    async def ttl(self, key):
        return await self.redis.ttl(self.generate_key(key))

    async def expire(self, key, timeout):
        return await self.redis.expire(self.generate_key(key), timeout)

    async def incr(self, key):
        return await self.redis.incr(self.generate_key(key))

    async def incrby(self, key, amount):
        return await self.redis.incrby(self.generate_key(key), amount)

    async def setnx(self, key, value):
        return await self.redis.setnx(self.generate_key(key), value)

    async def lpush(self, key, value, *values):
        return await self.redis.lpush(self.generate_key(key), value, *values)

    async def lrange(self, key, start, stop):
        return await self.redis.lrange(self.generate_key(key), start, stop)

    async def lrem(self, key, count, value):
        return await self.redis.lrem(self.generate_key(key), count, value)

    async def lset(self, key, index, value):
        return await self.redis.lset(self.generate_key(key), index, value)

    async def exists(self, key):
        return await self.redis.exists(self.generate_key(key))

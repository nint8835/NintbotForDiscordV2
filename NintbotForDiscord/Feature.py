import discord

from . import Bot
from .BasePlugin import BasePlugin


class Feature(object):

    def __init__(self, owner: BasePlugin, name: str, bot: "Bot.Bot"):
        self.bot = bot
        self.owner = owner
        self.name = name

    async def feature_enabled(self, server: discord.Server):
        storage = self.bot.RedisManager.get_storage(server)
        if await storage.exists("FEATURE:{}".format(self.name)):
            if await storage.get("FEATURE:{}".format(self.name)) == b"True":
                return True
            else:
                return False
        else:
            return False

    async def enable_feature(self, server: discord.Server):
        storage = self.bot.RedisManager.get_storage(server)
        await storage.set("FEATURE:{}".format(self.name), str(True))

    async def disable_feature(self, server: discord.Server):
        storage = self.bot.RedisManager.get_storage(server)
        await storage.set("FEATURE:{}".format(self.name), str(False))
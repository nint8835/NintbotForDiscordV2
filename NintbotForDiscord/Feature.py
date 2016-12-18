import discord

from . import Bot
from .BasePlugin import BasePlugin


class Feature(object):
    def __init__(self, owner: BasePlugin, name: str, bot: "Bot.Bot", description: str):
        self.bot = bot
        self.owner = owner
        self.name = name
        self.description = description

    async def feature_enabled(self, channel: discord.Channel=None, server: discord.Server=None):
        if channel is not None:
            if channel.is_private:
                return True
            else:
                server = channel.server
        if server is not None:
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

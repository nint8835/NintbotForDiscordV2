import os

from discord import Object

from NintbotForDiscord.BasePlugin import BasePlugin
from NintbotForDiscord import Bot
from NintbotForDiscord.Enums import EventType
from NintbotForDiscord.EventArgs import EventArgs, ServerJoinedEventArgs, ServerRemovedEventArgs, \
    ServerUnavailableEventArgs


class Plugin(BasePlugin):
    PLUGIN_NAME = "Logger"
    PLUGIN_DESCRIPTION = "A plugin that logs events."
    PLUGIN_VERSION = "1.2"
    PLUGIN_DEVELOPER = "nint8835"

    def __init__(self, bot: "Bot.Bot", folder: os.path):
        super(Plugin, self).__init__(bot, folder)
        self.channel_id = "199197365624766464"
        self.channel = Object(self.channel_id)

        self.bot.EventManager.register_handler(EventType.CLIENT_READY,
                                               self.on_ready,
                                               self)

        self.bot.EventManager.register_handler(EventType.SERVER_JOINED,
                                               self.on_server_joined,
                                               self)

        self.bot.EventManager.register_handler(EventType.SERVER_REMOVED,
                                               self.on_server_removed,
                                               self)

        self.bot.EventManager.register_handler(EventType.SERVER_UNAVAILABLE,
                                               self.on_server_unavailable,
                                               self)

        self.bot.EventManager.register_handler(EventType.SERVER_AVAILABLE,
                                               self.on_server_available,
                                               self)

    async def on_ready(self, args: EventArgs):
        await self.bot.send_message(self.channel, ":white_check_mark: Bot ready")

    async def on_resume(self, args: EventArgs):
        await self.bot.send_message(self.channel, ":arrows_counterclockwise: Connection resumed")

    async def on_server_joined(self, args: ServerJoinedEventArgs):
        await self.bot.send_message(self.channel,
                                    ":chart_with_upwards_trend: Bot joined new server\n\
                                    ```Name: {}\nID: {}\nOwner: {}```".format(args.server.name,
                                                                              args.server.id,
                                                                              args.server.owner.name))

    async def on_server_removed(self, args: ServerRemovedEventArgs):
        await self.bot.send_message(self.channel,
                                    ":chart_with_downwards_trend: Bot removed server\n\
                                    ```Name: {}\nID: {}\nOwner: {}```".format(args.server.name,
                                                                              args.server.id,
                                                                              args.server.owner.name))

    async def on_server_unavailable(self, args: ServerUnavailableEventArgs):
        await self.bot.send_message(self.channel,
                                    ":warning: Server unavailable\n\
                                    ```Name: {}\nRegion: {}```".format(
                                        args.server.name,
                                        args.server.region.name.capitalize().replace("Us_", "US ").replace("_", " ")))

    async def on_server_available(self, args: ServerUnavailableEventArgs):
        await self.bot.send_message(self.channel,
                                    ":ballot_box_with_check: Server available\n\
                                    ```Name: {}\nRegion: {}```".format(
                                        args.server.name,
                                        args.server.region.name.capitalize().replace("Us_", "US ").replace("_", " ")))

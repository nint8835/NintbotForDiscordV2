import os

from pprint import pprint

from NintbotForDiscord.BasePlugin import BasePlugin
from NintbotForDiscord.Enums import EventType
from NintbotForDiscord import Bot
from NintbotForDiscord.EventArgs import EventArgs, CommandReceivedEventArgs


class Plugin(BasePlugin):

    PLUGIN_NAME = "Test Plugin"
    PLUGIN_DESCRIPTION = "Tests various events"
    PLUGIN_VERSION = "1.0"
    PLUGIN_DEVELOPER = "nint8835"

    def __init__(self, bot: "Bot.Bot", folder: os.path):
        super(Plugin, self).__init__(bot, folder)

        self.bot.CommandManager.register_command("^say ([\w ]+)", self.test_command, self)

        for event_type in EventType:
            self.bot.EventManager.register_handler(event_type, self.print_event_info, self)

    @staticmethod
    async def print_event_info(args: EventArgs):
        pprint(vars(args))

    async def test_command(self, args: CommandReceivedEventArgs):
        await self.bot.send_message(args.channel, args.args[0])

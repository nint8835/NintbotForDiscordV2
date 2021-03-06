import json
import os
import random
import traceback

from NintbotForDiscord.BasePlugin import BasePlugin
from NintbotForDiscord import Bot
from NintbotForDiscord.EventArgs import CommandReceivedEventArgs


class Plugin(BasePlugin):
    PLUGIN_NAME = "Fanfiction"
    PLUGIN_DESCRIPTION = "Generates fanfiction based on users in the server"
    PLUGIN_VERSION = "1.3"
    PLUGIN_DEVELOPER = "nint8835"

    def __init__(self, bot: "Bot.Bot", folder: os.path):
        super(Plugin, self).__init__(bot, folder)
        with open(os.path.join(folder, "fanfiction.json")) as f:
            self.fanfiction = json.load(f)

        self.feature = self.bot.FeatureManager.register_feature(self, "fanfiction", "Allows generation of fanfictions.")

        self.bot.CommandManager.register_command("^generate (?:(?:a)|(?:some)) fanfiction",
                                                 self.generate_fanfiction,
                                                 self,
                                                 feature=self.feature)

    async def generate_fanfiction(self, args: CommandReceivedEventArgs):
        fanfiction = random.choice(self.fanfiction)
        users = []
        for i in range(fanfiction["members"]):
            looping = True
            while looping:
                user = random.choice([i for i in args.channel.server.members]).name
                if user not in users:
                    users.append(user)
                    looping = False
        await self.bot.send_message(args.channel, fanfiction["message"].format(users))


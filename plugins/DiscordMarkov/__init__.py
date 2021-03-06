import json
import logging
import os

import asyncio
import markovify

from NintbotForDiscord import Bot
from NintbotForDiscord.BasePlugin import BasePlugin
from NintbotForDiscord.Enums import EventType
from NintbotForDiscord.EventArgs import MessageReceivedEventArgs, CommandReceivedEventArgs
from NintbotForDiscord.Permissions.Special import Owner


class Plugin(BasePlugin):
    PLUGIN_NAME = "Discord Markov"
    PLUGIN_DESCRIPTION = "A plugin for generating messages based on previous messages using markov chains."
    PLUGIN_VERSION = "1.5.1"
    PLUGIN_DEVELOPER = "nint8835"

    def __init__(self, bot: "Bot.Bot", folder: os.path):
        super(Plugin, self).__init__(bot, folder)

        self.logger = logging.getLogger("DiscordMarkov")

        with open(os.path.join(self.plugin_folder, "data.json")) as f:
            self.data = json.load(f)

        self.make_chain()

        self.feature = self.bot.FeatureManager.register_feature(
            self,
            "markov",
            "Enables the use of the message generation capabilities of the bot."
        )

        self.bot.EventManager.register_handler(EventType.MESSAGE_RECEIVED, self.on_message, self)
        self.bot.CommandManager.register_command(
            "^(?:generate|make up|make me up|tell)(?: me)?(?: some)? (?:nonsense|wisdom)(?: based on | about )?\"?([\\w]+)?\"?\\.?$",
            self.wisdom_command,
            self,
            feature=self.feature
        )

        self.bot.CommandManager.register_command("^force a save$",
                                                 self.save_command,
                                                 self,
                                                 Owner())

        self.bot.EventManager.loop.create_task(self.save_and_regen())

    async def save_and_regen(self):
        while not self.bot.is_closed:
            self.logger.info("Saving data, do not shut down the bot.")
            with open(os.path.join(self.plugin_folder, "data.json"), "w") as f:
                json.dump(self.data, f)
            self.logger.info("Data saved. It is now safe to shut down the bot.")
            self.logger.debug("Regenerating chain.")
            await self.async_make_chain()
            self.logger.debug("Chain regenerated.")
            await asyncio.sleep(60)

    async def async_make_chain(self):
        generate_chain_task = self.bot.EventManager.loop.run_in_executor(None, self.make_chain)
        await generate_chain_task

    # noinspection PyAttributeOutsideInit
    def make_chain(self):
        self.chain = markovify.NewlineText("\n".join(self.data))

    async def on_message(self, args: MessageReceivedEventArgs):
        if args.content != "":
            self.data.append(args.content)

    def generate_message(self, start: str=""):
        message = ""
        count = 0
        # noinspection PyBroadException
        try:
            while message == "" and count < 5:
                if start != "":
                    message = self.chain.make_sentence_with_start(start)
                    count += 1
                else:
                    message = self.chain.make_sentence()
                    count += 1
        except:
            message = "I don't know how to respond."
        if message == "":
            message = "I don't know how to respond."
        return message

    async def wisdom_command(self, args: CommandReceivedEventArgs):
        if args.args[0] != "":
            await self.bot.send_message(args.channel, self.generate_message(args.args[0]))
        else:
            await self.bot.send_message(args.channel, self.generate_message())

    async def save_command(self, args: CommandReceivedEventArgs):
        with open(os.path.join(self.plugin_folder, "data.json"), "w") as f:
            json.dump(self.data, f)
        await self.bot.send_message(args.channel, "Data saved.")

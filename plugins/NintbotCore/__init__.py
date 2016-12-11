import os
import traceback

import discord
from discord import Game
from discord.utils import oauth_url

from NintbotForDiscord.BasePlugin import BasePlugin
from NintbotForDiscord import Bot
from NintbotForDiscord.Enums import EventType
from NintbotForDiscord.EventArgs import CommandReceivedEventArgs, EventArgs
from NintbotForDiscord.Permissions.Base import Administrator
from NintbotForDiscord.Permissions import MatchAnyPermissionGroup
from NintbotForDiscord.Permissions.Special import Owner


class Plugin(BasePlugin):

    PLUGIN_NAME = "Nintbot Core"
    PLUGIN_DESCRIPTION = "A collection of various core features"
    PLUGIN_VERSION = "1.5"
    PLUGIN_DEVELOPER = "nint8835"

    def __init__(self, bot: "Bot.Bot", folder: os.path):
        super(Plugin, self).__init__(bot, folder)

        self.manage_feature_permission = MatchAnyPermissionGroup(Owner(),
                                                                 Administrator())

        self.bot.EventManager.register_handler(EventType.CLIENT_READY, self.ready_event, self)

        self.bot.CommandManager.register_commands([
            "^how do I invite you$",
            "^how do I invite you to my server$",
            "^how do I add you$",
            "^how do I add you to my server$",
            "^how do I invite you\\?$",
            "^how do I invite you to my server\\?$",
            "^how do I add you\\?$",
            "^how do I add you to my server\\?$"
        ], self.invite_command, self)

        self.bot.CommandManager.register_commands([
            "^fix your current game$",
            "^reset your current game$"
        ], self.fix_game_command, self)

        self.bot.CommandManager.register_command("^how many servers are you (?:in|a member of|a part of)?[?]?$",
                                                 self.server_number_command,
                                                 self)

        self.bot.CommandManager.register_command("^enable (?:the (?:feature|module) )?(?:\")?([^\\n\"]+)(?:\")?",
                                                 self.enable_feature_command,
                                                 self,
                                                 self.manage_feature_permission)

        self.bot.CommandManager.register_command("^disable (?:the (?:feature|module) )?(?:\")?([^\\n\"]+)(?:\")?",
                                                 self.disable_feature_command,
                                                 self,
                                                 self.manage_feature_permission)

        self.bot.CommandManager.register_command("^(?:eval|execute|evaluate) ([^\n]+)$",
                                                 self.debug_command,
                                                 self,
                                                 Owner())

        self.bot.CommandManager.register_command("^what plugins (?:are enabled|do you have)[?]?",
                                                 self.plugins_command,
                                                 self)

        self.bot.CommandManager.register_command("^set your (?:currently )?(?:played )?game to \"?([^\\n\"]+)\"?$",
                                                 self.set_game_command,
                                                 self,
                                                 Owner(),
                                                 priority=1000)

    async def invite_command(self, args: CommandReceivedEventArgs):
        await self.bot.send_message(args.channel,
                                    "You can invite me to your server using the following link: {}".format(
                                        oauth_url(self.bot.client_id)
                                    ))

    async def ready_event(self, args: EventArgs):
        await self.bot.change_presence(game=Game(name="Nintbot V2 Beta"))

    async def fix_game_command(self, args: CommandReceivedEventArgs):
        await self.bot.change_presence(game=Game(name="Nintbot V2 Beta"))
        await self.bot.send_message(args.channel,
                                    "My currently displayed game should now be reset back to default.")

    async def server_number_command(self, args: CommandReceivedEventArgs):
        await self.bot.send_message(args.channel,
                                    "I am currently in {} servers.".format(len(self.bot.servers)))

    async def enable_feature_command(self, args: CommandReceivedEventArgs):
        storage = self.bot.RedisManager.get_storage(args.channel.server)
        await storage.set("FEATURE:{}".format(args.args[0]), str(True))
        await self.bot.send_message(args.channel,
                                    "The feature \"{}\" was enabled for this server.".format(args.args[0]))

    async def disable_feature_command(self, args: CommandReceivedEventArgs):
        storage = self.bot.RedisManager.get_storage(args.channel.server)
        await storage.set("FEATURE:{}".format(args.args[0]), str(False))
        await self.bot.send_message(args.channel,
                                    "The feature \"{}\" was disabled for this server.".format(args.args[0]))

    async def debug_command(self, args: CommandReceivedEventArgs):
        # noinspection PyBroadException
        try:
            await self.bot.send_message(args.channel,
                                        "```py\n{}```".format(eval(args.args[0])))
        except:
            await self.bot.send_message(args.channel,
                                        "```py\n{}```".format(traceback.format_exc(3)))

    async def plugins_command(self, args: CommandReceivedEventArgs):
        embed = discord.Embed()
        embed.colour = discord.Colour.blue()
        for plugin in self.bot.PluginManager.plugins:
            embed.add_field(name=plugin["instance"].PLUGIN_NAME, value="V{} by {}\n{}".format(
                plugin["instance"].PLUGIN_VERSION,
                plugin["instance"].PLUGIN_DEVELOPER,
                plugin["instance"].PLUGIN_DESCRIPTION
            ))
        await self.bot.send_message(args.channel, embed=embed)

    async def set_game_command(self, args: CommandReceivedEventArgs):
        # noinspection PyBroadException
        try:
            await self.bot.change_presence(game=Game(name=args.args[0]))
            await self.bot.send_message(args.channel, "My played game should now be set to \"{}\".".format(args.args[0]))
        except:
            traceback.print_exc(5)


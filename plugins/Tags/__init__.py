import os

from NintbotForDiscord.BasePlugin import BasePlugin
from NintbotForDiscord import Bot
from NintbotForDiscord.EventArgs import CommandReceivedEventArgs
from NintbotForDiscord.Permissions.Base import ManageMessages
from NintbotForDiscord.Permissions import MatchAnyPermissionGroup
from NintbotForDiscord.Permissions.Special import Owner


class Plugin(BasePlugin):

    PLUGIN_NAME = "Tags"
    PLUGIN_DESCRIPTION = "A system for making custom commands for displaying simple information."
    PLUGIN_VERSION = "1.0"
    PLUGIN_DEVELOPER = "nint8835"

    def __init__(self, bot: "Bot.Bot", folder: os.path):
        super(Plugin, self).__init__(bot, folder)

        self.bot.CommandManager.register_command('^what is (?:the value of )?(?:the key )?["]?([\\w \']+)["]?[?]?$',
                                                 self.get_tag_command,
                                                 self)

        self.bot.CommandManager.register_command(
            '^set (?:the value )?(?:of )?(?:the tag )?(?:")?([^\\n"]+)(?:")? to (?:")?([^\\n"]+)(?:")?$',
            self.set_tag_command,
            self
        )

        self.bot.CommandManager.register_command('^delete the tag (?:")?([^\\n"]+)(?:")?',
                                                 self.delete_tag_command,
                                                 self)

        self.set_tags_permission = MatchAnyPermissionGroup(Owner(), ManageMessages())

    async def get_tag_command(self, args: CommandReceivedEventArgs):
        if args.channel.is_private:
            storage = self.bot.RedisManager.get_storage(args.author)
        else:
            storage = self.bot.RedisManager.get_storage(args.channel.server)
        if await storage.exists("PLUGIN:TAG:{}".format(args.args[0])):
            await self.bot.send_message(args.channel,
                                        str(await storage.get("PLUGIN:TAG:{}".format(args.args[0])), "utf-8"))
        else:
            await self.bot.send_message(args.channel,
                                        "I can't seem to find that tag. Perhaps it belongs to a different server?")

    async def set_tag_command(self, args: CommandReceivedEventArgs):
        if args.channel.is_private:
            storage = self.bot.RedisManager.get_storage(args.author)
        else:
            if self.set_tags_permission.has_permission(args.author, args.channel):
                storage = self.bot.RedisManager.get_storage(args.channel.server)
            else:
                await self.bot.send_message(args.channel,
                                            "You do not have permission to create or edit tags in this channel. Sorry.")
                return
        await storage.set("PLUGIN:TAG:{}".format(args.args[0]), args.args[1])
        await self.bot.send_message(args.channel, "The value of that tag has been updated.")

    async def delete_tag_command(self, args: CommandReceivedEventArgs):
        if args.channel.is_private:
            storage = self.bot.RedisManager.get_storage(args.author)
        else:
            if self.set_tags_permission.has_permission(args.author, args.channel):
                storage = self.bot.RedisManager.get_storage(args.channel.server)
            else:
                await self.bot.send_message(args.channel,
                                            "You do not have permission to delete tags in this channel. Sorry.")
                return
        if await storage.exists("PLUGIN:TAG:{}".format(args.args[0])):
            await storage.delete("PLUGIN:TAG:{}".format(args.args[0]))
            await self.bot.send_message(args.channel, "That tag has been deleted.")

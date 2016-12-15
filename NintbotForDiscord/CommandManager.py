import logging
import re
from operator import itemgetter
from typing import List
import asyncio
import discord

from .Permissions.Base import Permission
from .EventArgs import CommandReceivedEventArgs
from .Enums import EventType
from .BasePlugin import BasePlugin
from .EventManager import EventManager


class CommandManager(object):
    def __init__(self, event_manager: EventManager):
        self._event_manager = event_manager
        self.logger = logging.getLogger("CommandManager")
        self.commands = []  # type: List[dict]

    def register_command(self, command_regex: str, handler: asyncio.coroutine, plugin: BasePlugin,
                         permission: Permission = Permission(), priority: int = 0):
        self.commands.append({
            "plugin": plugin,
            "handler": handler,
            "regex": re.compile(command_regex),
            "regex_string": command_regex,
            "permission": permission,
            "priority": priority
        })
        self.logger.debug("Command with regex \"{}\" registered by plugin {}.".format(command_regex,
                                                                                      plugin.PLUGIN_NAME))

    def register_commands(self, command_regexes: List[str], handler: asyncio.coroutine, plugin: BasePlugin,
                          permission: Permission = Permission(), priority: int = 0):
        for regex in command_regexes:
            self.register_command(regex, handler, plugin, permission, priority)

    async def process_command(self, message: discord.Message):
        if message.content.startswith("Nintbot, "):
            command = message.content.lstrip("Nintbot,").lstrip(" ")
            for registered_command in sorted(self.commands, key=itemgetter("priority"), reverse=True):
                if registered_command["regex"].match(command):
                    if registered_command["permission"].has_permission(message.author, message.channel):
                        await self._event_manager.queue.put({
                            "handler": registered_command["handler"],
                            "type": EventType.COMMAND_RECEIVED,
                            "plugin": registered_command["plugin"],
                            "args": CommandReceivedEventArgs(message, registered_command)
                        })
                        break

import asyncio
import logging
import os
import traceback

from .EventArgs import EventArgs
from .Enums import EventType
from .BasePlugin import BasePlugin
from . import Bot


class EventManager(object):

    def __init__(self, bot_instance: "Bot.Bot") -> None:
        self.logger = logging.getLogger("EventManager")
        self._handlers = []
        self._bot = bot_instance
        self.logger.debug("Getting event loop...")
        self.loop = asyncio.get_event_loop()
        self.logger.debug("Creating event queue...")
        self.queue = asyncio.Queue(loop=self.loop)
        self.loop.create_task(self.event_handle_loop())

    async def event_handle_loop(self):
        """
        The main loop that dispatches incoming events to all registered handlers
        """
        while not self._bot.is_closed:
            handler = await self.queue.get()
            self.logger.info("{} item(s) in event queue.".format(self.queue.qsize()))

            try:
                await asyncio.wait_for(handler["handler"](handler["args"]), timeout=30, loop=self.loop)

            except asyncio.TimeoutError:
                self.logger.warning(
                    "Handling of {} event from plugin {} timed out.".format(handler["type"],
                                                                            handler["plugin"].PLUGIN_NAME))

            except:
                channel = self._bot.PluginManager.get_plugin_instance_by_name("Logger").channel
                await self._bot.send_message(channel, "An exception occured while handling an event:\n```{}```".format(
                    traceback.format_exc(2)))

    def register_handler(self, event_type: EventType, event_handler: asyncio.coroutine, plugin: BasePlugin=None):
        """
        Registers an event handler
        :param event_type: The type of event handled by this handler
        :param event_handler: The coroutine that will handle this event
        :param plugin: The plugin instance this handler belongs to
        """
        if plugin is None:
            plugin = BasePlugin(self._bot, os.getcwd())
        self._handlers.append({"type": event_type,
                               "handler": event_handler,
                               "plugin": plugin})

    async def dispatch_event(self, event_type: EventType, event_args: EventArgs=EventArgs()):
        """
        Dispatches an event to all available event handlers
        :param event_type: The type of event to be dispatched
        :param event_args: The arguments of the event
        """
        for handler in self._handlers:
            if handler["type"] == event_type:
                await self.queue.put({
                    "handler": handler["handler"],
                    "type": event_type,
                    "args": event_args,
                    "plugin": handler["plugin"]
                })

import os

from . import Bot


class BasePlugin(object):

    PLUGIN_NAME = "Unnamed Plugin"
    PLUGIN_DESCRIPTION = "An unnamed plugin"
    PLUGIN_VERSION = "unknown"
    PLUGIN_DEVELOPER = "unknown"

    def __init__(self, bot_instance: "Bot.Bot", plugin_folder: os.path):
        self.bot = bot_instance
        self.plugin_folder = plugin_folder

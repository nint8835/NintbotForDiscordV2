import importlib.util
import json
import os
import traceback

from .BasePlugin import BasePlugin
from . import Bot
from typing import List


class PluginManager(object):

    def __init__(self, bot: "Bot.Bot"):
        self.bot = bot  # type: Bot.Bot
        self.plugins = []  # type: List[dict]

    def get_plugins_by_name(self, name: str) -> list:
        """
        Returns all plugins matching the name
        :param name: The name to match
        :return: The list of all plugins matching the name
        """
        return [plugin for plugin in self.plugins if plugin["instance"].PLUGIN_NAME == name]

    def get_plugin_by_name(self, name: str) -> dict:
        """
        Returns only one plugin matching the name
        :param name: The name to match
        :return: The plugin that matches the name
        """
        plugins = self.get_plugins_by_name(name)
        if len(plugins) == 1:
            return plugins[0]
        elif len(plugins) == 0:
            return None
        else:
            return None

    def get_plugin_instance_by_name(self, name: str) -> BasePlugin:
        """
        Returns the plugin instance that matches the name
        :param name: The name to match
        :return: The plugin instance that matches the name
        """
        return self.get_plugin_by_name(name)["instance"]

    def load_plugins(self):
        """
        Loads all plugins from the plugins directory
        """
        self.plugins = []
        for folder in [os.path.join("plugins", i) for i in os.listdir(os.path.join("plugins"))\
                       if os.path.isdir(os.path.join("plugins", i))]:
            if os.path.isfile(os.path.join(folder, "plugin.json")):
                with open(os.path.join(folder, "plugin.json")) as f:
                    plugin_data = json.load(f)
                    # noinspection PyBroadException
                    try:
                        spec = importlib.util.spec_from_file_location(
                            plugin_data["module_name"], os.path.join(folder, plugin_data["main_file"]))
                        self.bot.logger.debug("Loading plugin {} version {}, by {}...".format(
                            plugin_data["plugin_name"], plugin_data["plugin_version"], plugin_data["plugin_developer"]))
                        plugin = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(plugin)
                        plugin_instance = plugin.Plugin(self.bot, folder)
                        self.plugins.append({"info": plugin_data,
                                             "status": "loaded",
                                             "module": plugin,
                                             "instance": plugin_instance})
                        self.bot.logger.debug("Plugin loaded.")
                    except:
                        self.bot.logger.error("Plugin {} version {}, by {} failed to load".format(
                            plugin_data["plugin_name"], plugin_data["plugin_version"], plugin_data["plugin_developer"]))
                        self.plugins.append({"info": plugin_data,
                                             "status": "error",
                                             "exception": traceback.format_exc(5),
                                             "module": plugin})
                        print(self.plugins[-1]["exception"])

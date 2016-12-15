from .Feature import Feature
from .BasePlugin import BasePlugin
from . import Bot


class FeatureManager(object):

    def __init__(self, bot: "Bot.Bot"):
        self.bot = bot
        self.features = {}

    def register_feature(self, owner: BasePlugin, name: str):
        if name in self.features:
            return self.features[name]
        feature = Feature(owner, name, self.bot)
        self.features[name] = feature
        return feature

    def get_feature(self, name: str):
        return self.features[name]
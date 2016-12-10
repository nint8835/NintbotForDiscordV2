import discord

from .Base import Permission


class Owner(Permission):
    def has_permission(self, user: discord.User, channel: discord.Channel):
        return user.id == "106162668032802816"

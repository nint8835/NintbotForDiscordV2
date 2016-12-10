from typing import List

import discord


class Permission(object):
    # noinspection PyMethodMayBeStatic
    def has_permission(self, user: discord.User, channel: discord.Channel):
        return True


class PermissionGroup(Permission):

    def __init__(self, *args: List[Permission]):
        self.permissions = args

    def has_permission(self, user: discord.User, channel: discord.Channel):
        return True


class MatchAnyPermissionGroup(PermissionGroup):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        return any([i.has_permission(user, channel) for i in self.permissions])


class MatchAllPermissionGroup(PermissionGroup):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        return not any([not i.has_permission(user, channel) for i in self.permissions])

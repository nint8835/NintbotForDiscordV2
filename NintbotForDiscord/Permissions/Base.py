import discord

from . import Permission


class CreateInstantInvite(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).create_instant_invite
        else:
            return False


class KickMembers(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).kick_members
        else:
            return False


class BanMembers(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).ban_members
        else:
            return False


class Administrator(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).administrator
        else:
            return False


class ManageChannels(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).manage_channels
        else:
            return False


class ManageServer(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).manage_server
        else:
            return False


class ReadMessages(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).read_messages
        else:
            return True


class SendMessages(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).send_messages
        else:
            return True


class SendTTSMessages(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).send_tts_messages
        else:
            return False


class ManageMessages(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).manage_messages
        else:
            return False


class EmbedLinks(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).embed_links
        else:
            return True


class AttachFiles(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).attach_files
        else:
            return True


class ReadMessageHistory(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).read_message_history
        else:
            return True


class MentionEveryone(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).mention_everyone
        else:
            return False


class Connect(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).connect
        else:
            return False


class Speak(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).speak
        else:
            return False


class MuteMembers(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).mute_members
        else:
            return False


class DeafenMembers(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).deafen_members
        else:
            return False


class MoveMembers(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).move_members
        else:
            return False


class UseVoiceActivation(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).use_voice_activation
        else:
            return False


class ChangeNickname(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).change_nickname
        else:
            return False


class ManageNicknames(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).manage_nicknames
        else:
            return False


class ManageRoles(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).manage_roles
        else:
            return False


class ManageEmojis(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).manage_emojis
        else:
            return False


class ManageWebhooks(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).manage_webhooks
        else:
            return False


class UseExternalEmojis(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).external_emojis
        else:
            return False


class AddReactions(Permission):

    def has_permission(self, user: discord.User, channel: discord.Channel):
        if isinstance(user, discord.Member):
            return channel.permissions_for(user).add_reactions
        else:
            return False

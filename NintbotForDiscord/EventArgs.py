import datetime
import discord
from typing import List


class EventArgs(object):
    pass


class MessageReceivedEventArgs(EventArgs):

    def __init__(self, message: discord.Message):
        self.message = message  # type: discord.Message
        self.content = message.content  # type: str
        self.channel = message.channel  # type: discord.Channel
        self.author = message.author  # type: discord.User
        self.attachments = message.attachments  # type: List[str]


class PrivateMessageReceivedEventArgs(MessageReceivedEventArgs):

    def __init__(self, message: discord.Message):
        super(PrivateMessageReceivedEventArgs, self).__init__(message)
        self.channel = message.channel  # type: discord.PrivateChannel


class ServerMessageReceivedEventArgs(MessageReceivedEventArgs):

    def __init__(self, message: discord.Message):
        super(ServerMessageReceivedEventArgs, self).__init__(message)
        self.server = message.server  # type: discord.Server
        self.mentions = message.mentions  # type: List[discord.Member]


class MessageDeletedEventArgs(EventArgs):

    def __init__(self, message: discord.Message):
        self.message = message  # type: discord.Message
        self.channel = message.channel  # type: discord.Channel
        self.author = message.author  # type: discord.User
        self.content = message.content  # type: str
        self.attachments = message.attachments  # type: List[str]


class MessageEditedEventArgs(EventArgs):

    def __init__(self, before: discord.Message, after: discord.Message):
        self.message_before = before  # type: discord.Message
        self.message_after = after  # type: discord.Message
        self.content_before = before.content  # type: str
        self.content_after = after.content  # type: str
        self.channel = before.channel  # type: discord.Channel
        self.author = before.author  # type: discord.User


class ChannelDeletedEventArgs(EventArgs):

    def __init__(self, channel: discord.Channel):
        self.channel = channel  # type: discord.Channel
        self.name = channel.name  # type: str
        self.server = channel.server  # type: discord.Server


class ChannelCreatedEventArgs(EventArgs):

    def __init__(self, channel: discord.Channel):
        self.channel = channel  # type: discord.Channel
        self.name = channel.name  # type: str
        self.is_private = channel.is_private  # type: bool


class ChannelUpdatedEventArgs(EventArgs):

    def __init__(self, before: discord.Channel, after: discord.Channel):
        self.channel_before = before  # type: discord.Channel
        self.channel_after = after  # type: discord.Channel
        self.name_before = before.name  # type: str
        self.name_after = after.name  # type: str
        self.server = before.server  # type: discord.Server


class MemberJoinedEventArgs(EventArgs):

    def __init__(self, member: discord.Member):
        self.member = member  # type: discord.Member
        self.server = member.server  # type: discord.Server
        self.name = member.name  # type: str


class MemberRemovedEventArgs(EventArgs):

    def __init__(self, member: discord.Member):
        self.member = member  # type: discord.Member
        self.server = member.server  # type: discord.Server
        self.name = member.name  # type: str


class MemberUpdatedEventArgs(EventArgs):

    def __init__(self, before: discord.Member, after: discord.Member):
        self.server = before.server  # type: discord.Server
        self.member_before = before  # type: discord.Member
        self.member_after = after  # type: discord.Member
        self.name_before = before.name  # type: str
        self.name_after = after.name  # type: str
        self.display_name_before = before.display_name  # type: str
        self.display_name_after = after.display_name  # type: str
        self.status_before = before.status  # type: discord.Status
        self.status_after = after.status  # type: discord.Status
        self.game_before = before.game  # type: discord.Game
        self.game_after = after.game  # type: discord.Game


class MemberBannedEventArgs(EventArgs):

    def __init__(self, member: discord.Member):
        self.member = member  # type: discord.Member
        self.server = member.server  # type: discord.Server
        self.name = member.name  # type: str


class MemberUnbannedEventArgs(EventArgs):

    def __init__(self, server: discord.Server, user: discord.User):
        self.user = user  # type: discord.User
        self.server = server  # type: discord.Server
        self.user_name = user.name  # type: str
        self.server_name = server.name  # type: str


class MemberTypingEventArgs(EventArgs):

    def __init__(self, channel: discord.Channel, user: discord.User, when: datetime.datetime):
        self.channel = channel  # type: discord.Channel
        self.user = user  # type: discord.User
        self.when = when  # type: datetime.datetime


class ServerStatusBaseEventArgs(EventArgs):

    def __init__(self, server: discord.Server):
        self.server = server  # type: discord.Server


class ServerJoinedEventArgs(ServerStatusBaseEventArgs):
    pass


class ServerRemovedEventArgs(ServerStatusBaseEventArgs):
    pass


class ServerAvailableEventArgs(ServerStatusBaseEventArgs):
    pass


class ServerUnavailableEventArgs(ServerStatusBaseEventArgs):
    pass


class ServerUpdatedEventArgs(EventArgs):

    def __init__(self, before: discord.Server, after: discord.Server):
        self.before = before  # type: discord.Server
        self.after = after  # type: discord.Server


class RoleExistanceUpdatedBaseEventArgs(EventArgs):

    def __init__(self, server: discord.Server, role: discord.Role):
        self.server = server  # type: discord.Server
        self.role = role  # type: discord.Role


class RoleCreatedEventArgs(RoleExistanceUpdatedBaseEventArgs):
    pass


class RoleDeletedEventArgs(RoleExistanceUpdatedBaseEventArgs):
    pass


class RoleUpdatedEventArgs(EventArgs):

    def __init__(self, before: discord.Role, after: discord.Role):
        self.before = before  # type: discord.Role
        self.after = after  # type: discord.Role
        self.server = before.server  # type: discord.Server


class VoiceStateUpdatedEventArgs(MemberUpdatedEventArgs):

    def __init__(self, before: discord.Member, after: discord.Member):
        super(VoiceStateUpdatedEventArgs, self).__init__(before, after)
        self.voice_channel_before = before.voice_channel  # type: discord.Channel
        self.voice_channel_after = after.voice_channel  # type: discord.Channel
        self.self_mute_before = before.self_mute  # type: bool
        self.self_mute_after = after.self_mute  # type: bool
        self.mute_before = before.mute  # type: bool
        self.mute_after = after.mute  # type: bool
        self.self_deaf_before = before.self_deaf  # type: bool
        self.self_deaf_after = after.self_deaf  # type: bool
        self.deaf_before = before.deaf  # type: bool
        self.deaf_after = after.deaf  # type: bool


class CommandReceivedEventArgs(MessageReceivedEventArgs):

    def __init__(self, message: discord.Message, command_info: dict):
        super(CommandReceivedEventArgs, self).__init__(message)
        self.args = command_info["regex"].findall(self.content.lstrip("Nintbot, "))[0]
        if not isinstance(self.args, tuple):
            self.args = (self.args, )


class ReactionEditedEventArgs(EventArgs):

    def __init__(self, reaction: discord.Reaction, user: discord.User):
        self.reaction = reaction  # type: discord.Reaction
        self.user = user  # type: discord.User
        self.message = reaction.message  # type: discord.Message


class ReactionAddedEventArgs(ReactionEditedEventArgs):
    pass


class ReactionRemovedEventArgs(ReactionEditedEventArgs):
    pass


class ReactionsClearedEventArgs(EventArgs):

    def __init__(self, message: discord.Message, reactions: List[discord.Reaction]):
        self.message = message  # type: discord.Message
        self.reactions = reactions  # type: List[discord.Reaction]


class GroupMembershipStatusChangedEventArgs(EventArgs):

    def __init__(self, channel: discord.PrivateChannel, user: discord.User):
        self.channel = channel  # type: discord.PrivateChannel
        self.user = user  # type: discord.User


class MemberJoinedGroupEventArgs(GroupMembershipStatusChangedEventArgs):
    pass


class MemberRemovedFromGroupEventArgs(GroupMembershipStatusChangedEventArgs):
    pass


class ServerEmojisUpdatedEventArgs(EventArgs):

    def __init__(self, before: List[discord.Emoji], after: List[discord.Emoji]):
        self.before = before  # type: List[discord.Emoji]
        self.after = after  # type: List[discord.Emoji]

import datetime
import logging
from typing import Tuple
import discord

from .Redis import RedisManager
from .CommandManager import CommandManager
from .PluginManager import PluginManager
from .Enums import EventType
from .EventArgs import MessageReceivedEventArgs, PrivateMessageReceivedEventArgs, ServerMessageReceivedEventArgs, \
    MessageDeletedEventArgs, MessageEditedEventArgs, ChannelDeletedEventArgs, ChannelCreatedEventArgs, \
    ChannelUpdatedEventArgs, MemberJoinedEventArgs, MemberRemovedEventArgs, MemberUpdatedEventArgs, \
    MemberBannedEventArgs, MemberUnbannedEventArgs, MemberTypingEventArgs, ServerJoinedEventArgs, \
    ServerUnavailableEventArgs, ServerAvailableEventArgs, ServerRemovedEventArgs, ServerUpdatedEventArgs, \
    RoleCreatedEventArgs, RoleDeletedEventArgs, VoiceStateUpdatedEventArgs, RoleUpdatedEventArgs
from .EventManager import EventManager


class Bot(discord.Client):

    def __init__(self, token: str, client_id: str, redis_addr: Tuple[str, int], log_level=logging.INFO):
        super(Bot, self).__init__()

        logging.basicConfig(format="{%(asctime)s} (%(name)s) [%(levelname)s]: %(message)s",
                            datefmt="%x, %X",
                            level=log_level)

        self.client_id = client_id
        self._client_token = token

        self.logger = logging.getLogger("NintbotForDiscord")

        self.logger.debug("Creating EventManager...")
        self.EventManager = EventManager(self)

        self.logger.debug("Creating RedisManager...")
        self.RedisManager = RedisManager(self, redis_addr)

        self.logger.debug("Creating CommandManager...")
        self.CommandManager = CommandManager(self.EventManager)

        self.logger.debug("Creating PluginManager...")
        self.PluginManager = PluginManager(self)

        self.logger.info("Beginning load of plugins...")
        self.PluginManager.load_plugins()

        self.logger.debug("Silencing output from other modules...")
        logging.getLogger("discord").setLevel(logging.ERROR)
        logging.getLogger("websockets").setLevel(logging.ERROR)

    def start_bot(self):
        self.logger.info("Starting bot...")
        self.run(self._client_token)

    async def on_ready(self):
        self.logger.info("Bot ready.")
        await self.EventManager.dispatch_event(EventType.CLIENT_READY)

    async def on_resume(self):
        await self.EventManager.dispatch_event(EventType.CLIENT_RESUMED)

    async def on_message(self, message: discord.Message):
        await self.EventManager.dispatch_event(EventType.MESSAGE_RECEIVED,
                                               MessageReceivedEventArgs(message))

        await self.CommandManager.process_command(message)

        if message.channel.is_private:
            await self.EventManager.dispatch_event(EventType.PRIVATE_MESSAGE_RECEIVED,
                                                   PrivateMessageReceivedEventArgs(message))

        else:
            await self.EventManager.dispatch_event(EventType.SERVER_MESSAGE_RECEIVED,
                                                   ServerMessageReceivedEventArgs(message))

    async def on_message_delete(self, message: discord.Message):
        await self.EventManager.dispatch_event(EventType.MESSAGE_DELETED,
                                               MessageDeletedEventArgs(message))

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        await self.EventManager.dispatch_event(EventType.MESSAGE_EDITED,
                                               MessageEditedEventArgs(before, after))

    async def on_channel_delete(self, channel: discord.Channel):
        await self.EventManager.dispatch_event(EventType.CHANNEL_DELETED,
                                               ChannelDeletedEventArgs(channel))

    async def on_channel_create(self, channel: discord.Channel):
        await self.EventManager.dispatch_event(EventType.CHANNEL_CREATED,
                                               ChannelCreatedEventArgs(channel))

    async def on_channel_update(self, before: discord.Channel, after: discord.Channel):
        await self.EventManager.dispatch_event(EventType.CHANNEL_UPDATED,
                                               ChannelUpdatedEventArgs(before, after))

    async def on_member_join(self, member: discord.Member):
        await self.EventManager.dispatch_event(EventType.MEMBER_JOINED,
                                               MemberJoinedEventArgs(member))

    async def on_member_remove(self, member: discord.Member):
        await self.EventManager.dispatch_event(EventType.MEMBER_REMOVED,
                                               MemberRemovedEventArgs(member))

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        await self.EventManager.dispatch_event(EventType.MEMBER_UPDATED,
                                               MemberUpdatedEventArgs(before, after))

    async def on_member_ban(self, member: discord.Member):
        await self.EventManager.dispatch_event(EventType.MEMBER_BANNED,
                                               MemberBannedEventArgs(member))

    async def on_member_unban(self, server: discord.Server, user: discord.User):
        await self.EventManager.dispatch_event(EventType.MEMBER_UNBANNED,
                                               MemberUnbannedEventArgs(server, user))

    async def on_typing(self, channel: discord.Channel, user: discord.User, when: datetime.datetime):
        await self.EventManager.dispatch_event(EventType.MEMBER_TYPING,
                                               MemberTypingEventArgs(channel, user, when))

    async def on_server_join(self, server: discord.Server):
        await self.EventManager.dispatch_event(EventType.SERVER_JOINED,
                                               ServerJoinedEventArgs(server))

    async def on_server_remove(self, server: discord.Server):
        await self.EventManager.dispatch_event(EventType.SERVER_REMOVED,
                                               ServerRemovedEventArgs(server))

    async def on_server_available(self, server: discord.Server):
        await self.EventManager.dispatch_event(EventType.SERVER_AVAILABLE,
                                               ServerAvailableEventArgs(server))

    async def on_server_unavailable(self, server: discord.Server):
        await self.EventManager.dispatch_event(EventType.SERVER_UNAVAILABLE,
                                               ServerUnavailableEventArgs(server))

    async def on_server_update(self, before: discord.Server, after: discord.Server):
        await self.EventManager.dispatch_event(EventType.SERVER_UPDATED,
                                               ServerUpdatedEventArgs(before, after))

    async def on_server_role_create(self, server: discord.server, role: discord.Role):
        await self.EventManager.dispatch_event(EventType.ROLE_CREATED,
                                               RoleCreatedEventArgs(server, role))

    async def on_server_role_delete(self, server: discord.server, role: discord.Role):
        await self.EventManager.dispatch_event(EventType.ROLE_DELETED,
                                               RoleDeletedEventArgs(server, role))

    async def on_server_role_update(self, before: discord.Role, after: discord.Role):
        await self.EventManager.dispatch_event(EventType.ROLE_UPDATED,
                                               RoleUpdatedEventArgs(before, after))

    async def on_voice_state_update(self, before: discord.Member, after: discord.Member):
        await self.EventManager.dispatch_event(EventType.VOICE_STATE_UPDATED,
                                               VoiceStateUpdatedEventArgs(before, after))

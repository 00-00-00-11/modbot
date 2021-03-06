import sys
from typing import Dict, List

import aioredis
import discord
import discord.ext.commands
from discord.errors import Forbidden
from discord.guild import Guild
from discord.message import Message
from discord.reaction import Reaction
from discord.user import User

from shared import configuration
from shared.limited_dict import LimitedSizeDict


class Config():
    def __init__(self) -> None:
        pass

    @property
    def owners(self) -> List[str]:
        return configuration.get('owners')

class Bot(discord.ext.commands.Bot):
    def __init__(self) -> None:
        self.config = Config()
        super().__init__(command_prefix='~')
        super().load_extension('roles.colour')
        super().load_extension('discordbot.updater')
        super().load_extension('discordbot.botguild')
        super().load_extension('discordbot.owner')
        super().load_extension('discordbot.errors')
        super().load_extension('notices_channel')
        super().load_extension('honk')
        super().load_extension('spoilerchan.spoilers')


    def init(self) -> None:
        self.run(configuration.get('token'))

    async def on_ready(self) -> None:
        self.redis = await aioredis.create_redis_pool("redis://localhost", minsize=5, maxsize=10)
        print('Logged in as {username} ({id})'.format(username=self.user.name, id=self.user.id))
        print('Connected to {0}'.format(', '.join([server.name for server in self.guilds])))
        print('--------')

def init() -> None:
    client = Bot()
    client.init()

if __name__ == "__main__":
    init()

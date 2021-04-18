from datetime import datetime

import discord
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
from discord.guild import Guild
from discord.member import Member
from discord.role import Role


class Powerplay(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        print('Load Powerplay Cog')

    @tasks.loop(hours=1.0)
    async def powerplay_loop(self):
        time = datetime.utcnow()
        if time.weekday() == 3:
            if time.hour == 0:
                guild: Guild = self.bot.get_guild(662439414152167434)
                pp_role: Role = discord.utils.get(
                    guild.roles, name="PowerPlay")

                members_with_role: list[Member] = pp_role.members

                for member in members_with_role:
                    member.send(
                        content='**Reminder:** PowerPlay cycles in 1 day')

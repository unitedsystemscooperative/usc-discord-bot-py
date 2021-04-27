
import asyncio
import datetime
import logging
import math

import requests
from discord import Embed, TextChannel
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
from mongo import get_value, set_value

logging.basicConfig(level=logging.INFO)

TICK_API = 'https://elitebgs.app/api/ebgs/v5/ticks'
FACTION_API = 'https://elitebgs.app/api/ebgs/v5/factions?name=United%20Systems%20Cooperative'


class BGSCog(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        print("Load BGS Cog")
        self.watch_for_tick.start()

    def cog_unload(self):
        self.watch_for_tick.stop()

    @tasks.loop(hours=1)
    async def watch_for_tick(self):
        tick_time: str = requests.get(TICK_API).json()[0]['time']
        tick_time = tick_time.replace('Z', '')
        print(tick_time)
        last_tick = get_value('lastTick')

        if tick_time != last_tick:
            await self.send_tick_message(tick_time)
            set_value('lastTick', tick_time)
            await asyncio.sleep(3600)
            await self.send_systems_message()

    @watch_for_tick.before_loop
    async def _wait_for_bot(self):
        print('tick watcher waiting for bot...')
        await self.bot.wait_until_ready()

    async def send_tick_message(self, tick: str):
        ''' Builds and sends the 'Tick Detected' message '''
        tick_time = datetime.datetime.fromisoformat(tick)
        latest_tick_time = tick_time.time().isoformat(timespec='minutes')
        latest_tick_date = tick_time.date().isoformat()

        embed = Embed(title='Tick Detected')
        embed.add_field(name="Latest Tick at",
                        value=f"{latest_tick_time} UTC - {latest_tick_date}")
        embed.timestamp = datetime.datetime.now()
        channel: TextChannel = self.bot.get_channel(831261490258509935)
        await channel.send(embed=embed)

    async def send_systems_message(self):
        ''' Builds and sends the current system information '''
        data = requests.get(FACTION_API).json()
        presences = data['docs'][0]['faction_presence']
        channel: TextChannel = self.bot.get_channel(831261490258509935)

        i = 1
        embed = Embed(title='BGS Report')
        for presence in presences:
            if i == 25:
                await channel.send(embed=embed)
                embed = Embed(title='BGS Report Cont')
                i = 1
            system_name = presence['system_name']
            influence = "{:.1%}".format(presence['influence'])
            active_states = presence['active_states']
            pending_states = presence['pending_states']
            updated_at = presence['updated_at']
            faction_info = self.build_faction_info(
                influence, active_states, pending_states, updated_at)
            embed.add_field(name=system_name, value=faction_info)

            i += 1

        if len(presences) <= 25:
            await channel.send(embed=embed)

    @staticmethod
    def build_faction_info(influence: str, active_states: list[dict], pending_states: list[dict], updated_at: str) -> str:

        pass

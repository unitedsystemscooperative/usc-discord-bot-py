import json
import os
from datetime import datetime

import discord
from discord.user import User
import requests
from configs import INARA_API_URL, guild_ids
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
from ranks import ranks

from configs import test_guild_ids


class InaraCommands(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        print('Load Inara Commands Cog')

    @cog_ext.cog_slash(name='cmdr',
                       description="gives a description of the cmdr from inara",
                       options=[create_option(
                           name='cmdr', description="cmdr name", option_type=3, required=True)])
    async def _cmdr(self, ctx: SlashContext, cmdr: str):
        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        await ctx.defer()

        api_key = os.getenv('INARA_TOKEN', '')

        request_header = {'appName': 'USC Bot', 'appVersion': '1.0.0',
                          'isBeingDeveloped': 'true', 'APIkey': api_key}
        request_event = [{'eventName': 'getCommanderProfile',
                          'eventTimestamp': current_time, 'eventData': {'searchName': cmdr}}]
        data = {'header': request_header, 'events': request_event}
        json_data = json.dumps(data)
        response = requests.post(
            INARA_API_URL, data=json_data).json()

        response_code: int = response['events'][0]['eventStatus']

        if response_code == 204:
            await ctx.send("No inara profiles were found")
            return
        if response_code == 400:
            await ctx.send("There was an error executing that command")
            return

        try:
            cmdr_info = response['events'][0]['eventData']
            cmdr_ranks = cmdr_info['commanderRanksPilot']
            embed = discord.Embed(
                title='Inara Profile', url=cmdr_info['inaraURL'], description=f"Role: {cmdr_info.get('preferredGameRole', 'N/A')}")
            embed.set_author(name=cmdr_info['commanderName'],
                             url=cmdr_info['inaraURL'])
            if 'avatarImageURL' in cmdr_info:
                embed.set_thumbnail(url=cmdr_info['avatarImageURL'])
            for cmdr_rank in cmdr_ranks:
                rank_name: str = cmdr_rank['rankName']
                rank_value: int = int(cmdr_rank['rankValue'])
                rank_value_s: str = ranks[rank_name][rank_value]
                rank_progress = '' if rank_value_s == 'Elite' or rank_value_s == 'King' or rank_value_s == 'Admiral' else f"- {int(float(cmdr_rank['rankProgress']) *100)} %"
                embed.add_field(name=f"{rank_name.capitalize()} Rank",
                                value=f"{rank_value_s} {rank_progress}")

            if 'commanderSquadron' in cmdr_info:
                squad_info = cmdr_info['commanderSquadron']
                embed.add_field(
                    name="Squadron", value=f"{squad_info['squadronName']} - {squad_info['inaraURL']}", inline=False)

            embed.set_footer(
                text=f"Retrieved from Inara at the behest of {ctx.author.display_name}")
            await ctx.send(embed=embed)
        except discord.errors.NotFound:
            print('there was an error with the discord system')

    @cog_ext.cog_slash(name="squadron",
                       description="gives in-game squadron and suggests inara",
                       options=[create_option('user', description='user to send to', option_type=6, required=False)])
    async def _squadron(self, ctx: SlashContext, user: User = None):
        message = "To join the squadron, go to your right hand panel, click on the squadron button, search **USPC** in the search bar, and you should find us!\n\nAfter you've joined in-game, you are also free to join our inara squadron!\nhttps://inara.cz/squadron/7028/"
        if user:
            await user.send(message)
            await ctx.send('message sent to user', hidden=True)
        else:
            await ctx.send(message)

""" Discord Bot entrypoint """
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from commands import load_commands
from keep_alive import keep_alive

load_dotenv()
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

load_commands(bot)

keep_alive()


@bot.event
async def on_ready():
    print('Bot Online')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Eolin's Video"))

bot.run(os.getenv('BOT_TOKEN'))

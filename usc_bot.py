""" Discord Bot entrypoint """
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from commands import load_commands

load_dotenv()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


load_commands(bot)

bot.description = "Being developed"


bot.run(os.getenv('BOT_TOKEN'))

""" Discord Bot entrypoint """
import os

import discord
from discord.ext import commands
from discord_slash.client import SlashCommand
from dotenv import load_dotenv

from cogs import (AdminCommands, EducationalCommands, FunCommands, GalNet,
                  InaraCommands, Powerplay)
from keep_alive import keep_alive

load_dotenv()
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(bot, override_type=True, sync_commands=True)

bot.add_cog(AdminCommands(bot))
bot.add_cog(EducationalCommands(bot))
bot.add_cog(FunCommands(bot))
bot.add_cog(InaraCommands(bot))
bot.add_cog(GalNet(bot))
bot.add_cog(Powerplay(bot))


is_prod = os.getenv("IS_PROD", None)
if is_prod:
    keep_alive()


@bot.event
async def on_ready():
    ''' Event when the bot is ready '''
    print('Bot Online')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Eolin's Video"))

bot.run(os.getenv('BOT_TOKEN'))

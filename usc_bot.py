""" Discord Bot entrypoint """
import os

import bugsnag
import logging
from bugsnag.handlers import BugsnagHandler
import discord
from discord.ext import commands
from discord_slash.client import SlashCommand
from dotenv import load_dotenv

from cogs import (AdminCommands, BGSCog, DevCommands, EducationalCommands,
                  FunCommands, GankCommands, GalNet, InaraCommands, Powerplay, UtilCommands)

load_dotenv()

bugsnag_key = os.environ.get("BUGSNAG_TOKEN")
bugsnag.configure(api_key=bugsnag_key, project_root='.')
logger = logging.getLogger()
handler = BugsnagHandler()
handler.setLevel(logging.ERROR)
logger.addHandler(handler)

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(bot, override_type=True, sync_commands=True)

bot.add_cog(AdminCommands(bot))
bot.add_cog(DevCommands(bot))
bot.add_cog(EducationalCommands(bot))
bot.add_cog(FunCommands(bot))
bot.add_cog(GankCommands(bot))
bot.add_cog(InaraCommands(bot))
bot.add_cog(UtilCommands(bot))
bot.add_cog(BGSCog(bot))
bot.add_cog(GalNet(bot))
bot.add_cog(Powerplay(bot))


@bot.event
async def on_ready():
    ''' Event when the bot is ready '''
    print('Bot Online')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Eolin's Video"))


@bot.event
async def on_error(event, *args, **kwargs):
    bugsnag.notify(Exception(f'There was an error in {event}.', args, kwargs))

bot.run(os.getenv('BOT_TOKEN'))

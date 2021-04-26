import discord
from configs import guild_ids, test_guild_ids
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.user import User
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option


class DevCommands(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        print('Load Dev Commands Cog')

    @cog_ext.cog_subcommand(base='dev', name='github-website',
                            description='Get the link to the github for https://unitedsystems.org',
                            guild_ids=guild_ids,
                            options=[
                                create_option(
                                    name='user',
                                    description='Send this to a user instead of public',
                                    option_type=6,
                                    required=False
                                )
                            ])
    async def _github_website(self, ctx: SlashContext, user: User = None):
        message = "The website's github is https://github.com/admiralfeb/usc-website"
        if user:
            await user.send(message)
            await ctx.send('Sent to cmdr', hidden=True)
        else:
            await ctx.send(message)

    @cog_ext.cog_subcommand(base='dev', name='github-bot',
                            description='Get the link to the github for the USC Bot',
                            guild_ids=guild_ids,
                            options=[
                                create_option(
                                    name='user',
                                    description='Send this to a user instead of public',
                                    option_type=6,
                                    required=False
                                )
                            ])
    async def _github_bot(self, ctx: SlashContext, user: User = None):
        message = "The bot's github is https://github.com/admiralfeb/usc-discord-bot"
        if user:
            await user.send(message)
            await ctx.send('Sent to cmdr', hidden=True)
        else:
            await ctx.send(message)

    @cog_ext.cog_subcommand(base='dev', name='test_exception', description='sends an exception', guild_ids=test_guild_ids)
    async def _dev_test_exception(self, ctx: SlashContext):
        raise Exception('test exception from command', ctx)

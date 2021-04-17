import discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord_slash import SlashContext, cog_ext


class FunCommands(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        print('Load Fun Commands Cog')

    @cog_ext.cog_slash(name="caniscthere", description="Can I supercruise there?")
    async def _can_i_sc_there(self, ctx: SlashContext):
        await ctx.send(
            "Check this out: http://caniflytothenextstarinelitedangero.us/")

    @cog_ext.cog_slash(name="gifheresy", description="Stop your heresy")
    async def _gif_heresy(self, ctx: SlashContext):
        await ctx.send(
            "https://tenor.com/view/cease-your-heresy-warhammer-40k-gif-19005947"
        )

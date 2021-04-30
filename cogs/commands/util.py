import discord
from discord.channel import TextChannel
from discord.embeds import Embed
from discord.message import Message
from discord.reaction import Reaction
from configs import guild_ids, test_guild_ids
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.user import User
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option


class UtilCommands(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        print('Load Util Commands Cog')

    @cog_ext.cog_subcommand(base='util', name='viewDiscordLink',
                            description='Returns the discord link',
                            guild_ids=guild_ids)
    async def _view_discord_link(self, ctx: SlashContext):
        await ctx.send('https://discord.gg/HsmJpG3SkZ')

    @cog_ext.cog_subcommand(base="util",
                            name='viewEmbedSource',
                            description='Displays the embed source of a specific message',
                            guild_ids=guild_ids,
                            options=[create_option(name='messageID', description='ID of the message', option_type=3, required=True),
                                     create_option(name='channel', description='Channel the message was in', option_type=7, required=True)])
    async def _view_embed_source(self, ctx: SlashContext, messageID: int, channel: discord.TextChannel):
        message: Message = await channel.fetch_message(messageID)
        embeds: list[Embed] = message.embeds
        channel_to_respond_in: TextChannel = self.bot.get_channel(
            ctx.channel_id)

        if len(embeds) > 0:
            for embed in embeds:
                embed_dic = str(embed.to_dict())
                new_embed = Embed(title='Embed Source',
                                  description=f"""```{embed_dic}```""")
                await channel_to_respond_in.send(embed=new_embed)
            await ctx.send('done', hidden=True)
        else:
            await ctx.send('No embeds found', hidden=True)

    @cog_ext.cog_subcommand(base="util", name="poll_show",
                            description="Shows the results of a poll", guild_ids=guild_ids,
                            options=[create_option(name='messageID', description='ID of the message', option_type=3, required=True),
                                     create_option(name='channel', description='Channel the message was in', option_type=7, required=True)])
    async def _poll_show(self, ctx: SlashContext, messageId: int, channel: discord.TextChannel):
        message: Message = await channel.fetch_message(messageId)
        embeds: list[Embed] = message.embeds
        reactions: list[Reaction] = message.reactions

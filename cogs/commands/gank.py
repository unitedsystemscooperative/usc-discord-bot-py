import discord
from configs import guild_ids
from discord.channel import TextChannel
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.message import Message, PartialMessage
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
from mongo import get_value, set_value


class GankCommands(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        print('Load Gank Report Cog')

    @staticmethod
    def _check_auth(author_id: str, authorized_users: list = None) -> bool:
        ''' Checks if the user is authorized '''
        if authorized_users is not None:
            if next((auth_user for auth_user in authorized_users if auth_user['id'] == author_id), None) is not None:
                return True
        else:
            auth_users: list = get_value('authorized_users')
            if next((auth_user for auth_user in auth_users if auth_user['id'] == author_id), None) is not None:
                return True
        return False

    @staticmethod
    def generate_ganker_embed(gankers: list[str]) -> Embed:
        ''' Generates the ganker embed from the ganker list '''
        gankers.reverse()
        ganker_string = ''
        for ganker in gankers:
            ganker_string += ganker + '\n'
        ganker_embed = Embed()
        ganker_embed.add_field(name="Known Gankers", value=ganker_string)
        return ganker_embed

    def get_base_message(self) -> PartialMessage:
        ''' Gets the base report message for editing '''
        base_channel_id: int = int(get_value("gank_report_channel"))
        base_message_id: int = int(get_value("gank_report_message"))
        base_channel: TextChannel = self.bot.get_channel(base_channel_id)
        base_message: PartialMessage = base_channel.get_partial_message(
            base_message_id)
        return base_message

    @cog_ext.cog_subcommand(base="ganker", name="baseMessage", description="Set the base message in the gank report channel", guild_ids=guild_ids)
    async def _set_base_message(self, ctx: SlashContext):
        author_id = str(ctx.author.id)
        authorized_users: list = get_value('authorized_users')
        await ctx.defer(hidden=True)

        # Check if authorized
        if self._check_auth(author_id, authorized_users) is False:
            await ctx.send('Unauthorized to change gank list', hidden=True)
            return

        gank_report_channel: TextChannel = ctx.channel

        sent_message: Message = await gank_report_channel.send("Gank Report Base Message ... More to come")
        set_value("gank_report_channel", str(gank_report_channel.id))
        set_value("gank_report_message", str(sent_message.id))
        await ctx.send("Base message sent", hidden=True)

    @cog_ext.cog_subcommand(base="ganker", name="add", description="Adds a ganker to the list", guild_ids=guild_ids,
                            options=[create_option(name="gankername", description="name of ganker", option_type=3, required=True)])
    async def _add_ganker(self, ctx: SlashContext, gankername: str):
        author_id = str(ctx.author.id)
        authorized_users: list = get_value('authorized_users')
        await ctx.defer(hidden=True)

        if self._check_auth(author_id, authorized_users) is False:
            await ctx.send('Unauthorized to change ganker list', hidden=True)
            return

        gankers: list[str] = get_value("gankers")
        if gankers is None:
            gankers = []

        found_ganker = next(
            (x for x in gankers if x.lower() == gankername.lower()), None)
        if found_ganker is None:
            gankers.append(gankername)
            set_value("gankers", gankers)
        else:
            await ctx.send("Ganker is already in list", hidden=True)
            return

        ganker_embed = self.generate_ganker_embed(gankers)

        base_message = self.get_base_message()

        await base_message.edit(content=None, embed=ganker_embed)
        await ctx.send("Successfully added ganker", hidden=True)

    @cog_ext.cog_subcommand(base="ganker", name="remove", description="Removes a ganker from the list", guild_ids=guild_ids,
                            options=[create_option(name="gankername", description="name of ganker", option_type=3, required=True)])
    async def _remove_ganker(self, ctx: SlashContext, gankername: str):
        author_id = str(ctx.author.id)
        authorized_users: list = get_value('authorized_users')
        await ctx.defer(hidden=True)

        if self._check_auth(author_id, authorized_users) is False:
            await ctx.send('Unauthorized to change ganker list', hidden=True)
            return

        gankers: list[str] = get_value("gankers")
        if gankers is None:
            gankers = []

        found_ganker = next(
            (x for x in gankers if x.lower() == gankername.lower()), None)
        if found_ganker is not None:
            gankers.remove(found_ganker)
        else:
            await ctx.send("Ganker list unchanged. unable to find ganker", hidden=True)
            return

        ganker_embed = self.generate_ganker_embed(gankers)

        base_message = self.get_base_message()

        await base_message.edit(content=None, embed=ganker_embed)
        await ctx.send("Successfully removed ganker", hidden=True)

    @cog_ext.cog_subcommand(base="ganker", name="update", description="Updates the list in discord from the database", guild_ids=guild_ids)
    async def _update_gankers(self, ctx: SlashContext):
        await ctx.defer(hidden=True)

        gankers: list[str] = get_value("gankers")
        if gankers is None:
            gankers = []

        ganker_embed = self.generate_ganker_embed(gankers)
        base_message = self.get_base_message()

        await base_message.edit(content=None, embed=ganker_embed)
        await ctx.send("Successfully updated gankers from database", hidden=True)

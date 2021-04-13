""" Handles commands for the Discord bot """
import discord
from discord.ext.commands.bot import Bot
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option


def load_commands(bot: Bot):
    """ Loads slash commands for use in the Discord bot"""
    slash = SlashCommand(bot, sync_commands=True)
    test_guild_ids = [181594027945099264]
    guild_ids = [662439414152167434]

    @slash.slash(name="bot_announce_myself", description="Can only be used by Admiralfeb. Announces the bot.", guild_ids=test_guild_ids)
    async def _bot_announce_myself(ctx: SlashContext):
        author = ctx.author
        if author.id != 138029803214209025:
            pass
        else:
            embed = discord.Embed(title="Introducing Me!")
            embed.description = "I'm the USC Discord Bot!\n\nAfter talking to other squads and seeing their bots in action, Admiralfeb made me."

    @slash.slash(name='can_i_sc_there', guild_ids=guild_ids)
    async def _can_i_sc_there(ctx: SlashContext):
        await ctx.send("Check this out: http://caniflytothenextstarinelitedangero.us/")

    @slash.slash(name='fsd_booster', description=''' Links to Exegious' video on how to unlock the Guardian FSD Booster ''', guild_ids=guild_ids)
    async def _fsd_booster(ctx: SlashContext):
        await ctx.send("Here's how to unlock the guardian fsd booster: https://youtu.be/J9C9a00-rkQ")

    @slash.slash(
        name='neutron',
        description='Gives tutorials on how to use the neutron highway',
        guild_ids=guild_ids,
        options=[create_option(
            name='option', description="Choose what you'd like to know about the Neutron Highway",
            option_type=3, required=True,
            choices=[
                create_choice(value='img', name='Image Tutorial'),
                create_choice(value='spansh', name="Spansh's Website"),
                create_choice(value='desktop', name='Download an app'),
            ]
        )])
    async def _neutron(ctx: SlashContext, option: str):
        if option == 'img':
            await ctx.send("https://i.imgur.com/gg6n5VM.jpg")
        elif option == 'spansh':
            await ctx.send("Plot neutron highway routes online here: https://www.spansh.co.uk/plotter")
        else:
            await ctx.send("Desktop client for neutron routing here: https://github.com/winneon/neutron")

    @slash.slash(name="squadron", description="gives in-game squadron and suggests inara", guild_ids=guild_ids)
    async def _squadron(ctx: SlashContext):
        await ctx.send("To join the squadron, go to your right hand panel, click on the squadron button, search **USPC** in the search bar, and you should find us!\n\nAfter you've joined in-game, you are also free to join our inara squadron!\nhttps://inara.cz/squadron/7028/")

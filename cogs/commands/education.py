import discord
from configs import guild_ids, test_guild_ids
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.user import User
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option


class EducationalCommands(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        print('Load Educational Commands Cog')

    @cog_ext.cog_subcommand(base="edu",
                            name='fsd-booster',
                            description=''' Links to Exegious' video on how to unlock the Guardian FSD Booster ''',
                            options=[
                                create_option(
                                    name='user',
                                    description="Send this to a cmdr instead of public",
                                    option_type=6,
                                    required=False)])
    async def _fsd_booster(self, ctx: SlashContext, user: User = None):
        message = "Here's how to unlock the guardian fsd booster: https://youtu.be/J9C9a00-rkQ"
        if user:
            await user.send(message)
            await ctx.send('Sent to cmdr', hidden=True)
            return
        await ctx.send(message)

    @cog_ext.cog_subcommand(base="edu",
                            name='neutron',
                            description='Gives tutorials on how to use the neutron highway',
                            options=[
                                create_option(
                                    name='option',
                                    description="Choose what you'd like to know about the Neutron Highway",
                                    option_type=3,
                                    required=True,
                                    choices=[
                                        create_choice(
                                            value='img', name='Image Tutorial'),
                                        create_choice(
                                            value='spansh', name="Spansh's Website"),
                                        create_choice(
                                            value='desktop', name='Download an app'),
                                    ]),
                                create_option(
                                    name='user',
                                    description="Send this to a cmdr instead of public",
                                    option_type=6,
                                    required=False)
                            ])
    async def _neutron(self, ctx: SlashContext, option: str, user: User = None):
        if user:
            if option == 'img':
                await user.send("https://i.imgur.com/gg6n5VM.jpg")
            elif option == 'spansh':
                await user.send(
                    "Plot neutron highway routes online here: https://www.spansh.co.uk/plotter"
                )
            else:
                await user.send(
                    "Desktop client for neutron routing here: https://github.com/winneon/neutron"
                )
            await ctx.send("Neutron info sent to the user", hidden=True)
        else:
            if option == 'img':
                await ctx.send("https://i.imgur.com/gg6n5VM.jpg")
            elif option == 'spansh':
                await ctx.send(
                    "Plot neutron highway routes online here: https://www.spansh.co.uk/plotter"
                )
            else:
                await ctx.send(
                    "Desktop client for neutron routing here: https://github.com/winneon/neutron"
                )

    @cog_ext.cog_subcommand(base='edu', name='promotions', description="how do I get promoted?",
                            options=[
                                create_option(
                                    name='user',
                                    description="Send this to a cmdr instead of public",
                                    option_type=6,
                                    required=False)
                            ])
    async def _promotions(self, ctx: SlashContext, user: User = None):
        embed = discord.Embed(title="How do I get promoted?")
        embed.add_field(
            name='Ensign', value='You must have spent at least one week in squad and you\'ve joined the squad in-game and in Discord')
        embed.add_field(
            name='Lieutenant', value="Ensign requirements + You've joined the Inara squad and have a good understanding of the game/engineers")
        embed.add_field(name='Lt. Commander',
                        value='Lieutenant + joined the mentorship mission on Inara and have been approved by High Command')
        embed.add_field(
            name='Captain + ', value="Selected from the Lt. Cmdrs and offered the role of High Command.")

        if user:
            await user.send(embed=embed)
            await ctx.send(content='Info sent to user', hidden=True)
        else:
            await ctx.send(embed=embed)

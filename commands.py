""" Handles commands for the Discord bot """
import discord
from discord.ext.commands.bot import Bot
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

from mongo import get_value, set_value


def load_commands(bot: Bot):
    """ Loads slash commands for use in the Discord bot"""
    slash = SlashCommand(bot, sync_commands=True)
    test_guild_ids = [181594027945099264]
    guild_ids = [181594027945099264, 662439414152167434]

    @slash.slash(name='botModifyAuthUsers',
                 description='Add/Delete authorized users for this bot',
                 guild_ids=guild_ids,
                 options=[
                     create_option(name='action',
                                   description="Add or Delete a user?",
                                   option_type=3,
                                   required=True,
                                   choices=[
                                       create_choice(value='add', name='Add'),
                                       create_choice(value='delete',
                                                     name='Delete'),
                                   ]),
                     create_option(
                         name='user',
                         description='tag the user you wish to change',
                         option_type=6,
                         required=True)
                 ])
    async def _bot_modify_auth_users(ctx: SlashContext, action: str,
                                     user: discord.User):
        author_id = str(ctx.author.id)
        authorized_users: list = get_value('authorized_users')
        print(author_id)
        print(authorized_users)

        # Check if authorized
        if next(
            (auth_user
             for auth_user in authorized_users if auth_user['id'] == author_id),
                None) is None:
            await ctx.send('Unauthorized to change authorized users')
            return

        if action == 'add':
            new_user = {}
            new_user['id'] = str(user.id)
            new_user['name'] = user.name
            new_user['discriminator'] = user.discriminator

            # Check if user is present in the list already
            if next((auth_user for auth_user in authorized_users
                     if auth_user['id'] == new_user['id']), None):
                await ctx.send(
                    f'{user.display_name} is already in authorized users')
                return

            authorized_users.append(new_user)
            set_value('authorized_users', authorized_users)
            await ctx.send(
                f'{user.display_name} added successfully to authorized users')
            return

        if action == 'delete':
            if len(authorized_users) == 1:
                await ctx.send(
                    'Unable to remove user as they are the last one.')
                return

            user_to_delete = next((auth_user for auth_user in authorized_users
                                   if auth_user['id'] == user.id), None)

            if user_to_delete is None:
                await ctx.send(
                    f'Unable to Delete: {user.display_name} does not exist authorized users'
                )
                return

            authorized_users.remove(user_to_delete)
            set_value('authorized_users', authorized_users)
            await ctx.send(f'Removed {user.display_name} from authorized users'
                           )
            return

        await ctx.send(
            'Error during authorized users change. Please check your inputs.')

    @slash.slash(name='can_i_sc_there', guild_ids=guild_ids)
    async def _can_i_sc_there(ctx: SlashContext):
        await ctx.send(
            "Check this out: http://caniflytothenextstarinelitedangero.us/")

    @slash.slash(
        name='fsd_booster',
        description=
        ''' Links to Exegious' video on how to unlock the Guardian FSD Booster ''',
        guild_ids=guild_ids)
    async def _fsd_booster(ctx: SlashContext):
        await ctx.send(
            "Here's how to unlock the guardian fsd booster: https://youtu.be/J9C9a00-rkQ"
        )

    @slash.slash(name="gif_heresy",
                 description="Stop your heresy",
                 guild_ids=guild_ids)
    async def _gif_heresy(ctx: SlashContext):
        await ctx.send(
            "https://tenor.com/view/cease-your-heresy-warhammer-40k-gif-19005947"
        )

    @slash.slash(
        name='neutron',
        description='Gives tutorials on how to use the neutron highway',
        guild_ids=guild_ids,
        options=[
            create_option(
                name='option',
                description=
                "Choose what you'd like to know about the Neutron Highway",
                option_type=3,
                required=True,
                choices=[
                    create_choice(value='img', name='Image Tutorial'),
                    create_choice(value='spansh', name="Spansh's Website"),
                    create_choice(value='desktop', name='Download an app'),
                ])
        ])
    async def _neutron(ctx: SlashContext, option: str):
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

    @slash.slash(name="squadron",
                 description="gives in-game squadron and suggests inara",
                 guild_ids=guild_ids)
    async def _squadron(ctx: SlashContext):
        await ctx.send(
            "To join the squadron, go to your right hand panel, click on the squadron button, search **USPC** in the search bar, and you should find us!\n\nAfter you've joined in-game, you are also free to join our inara squadron!\nhttps://inara.cz/squadron/7028/"
        )

import discord
from configs import guild_ids, test_guild_ids
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from mongo import get_value, set_value


class AdminCommands(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        print('Load Admin Commands Cog')

    @cog_ext.cog_slash(name='botModifyAuthUsers',
                       description='Add/Delete authorized users for this bot',
                       guild_ids=guild_ids,
                       options=[
                           create_option(name='action',
                                         description="Add or Delete a user?",
                                         option_type=3,
                                         required=True,
                                         choices=[
                                             create_choice(
                                                 value='add', name='Add'),
                                             create_choice(value='delete',
                                                           name='Delete'),
                                         ]),
                           create_option(
                               name='user',
                               description='tag the user you wish to change',
                               option_type=6,
                               required=True)
                       ])
    async def _bot_modify_auth_users(self, ctx: SlashContext, action: str,
                                     user: discord.User):
        author_id = str(ctx.author.id)
        authorized_users: list = get_value('authorized_users')
        print(author_id)
        print(authorized_users)
        await ctx.defer(hidden=True)

        # Check if authorized
        if next(
            (auth_user
             for auth_user in authorized_users if auth_user['id'] == author_id),
                None) is None:
            await ctx.send('Unauthorized to change authorized users', hidden=True)
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
                    f'{user.display_name} is already in authorized users', hidden=True)
                return

            authorized_users.append(new_user)
            set_value('authorized_users', authorized_users)
            await ctx.send(
                f'{user.display_name} added successfully to authorized users', hidden=True)
            return

        if action == 'delete':
            if len(authorized_users) == 1:
                await ctx.send(
                    'Unable to remove user as they are the last one.', hidden=True)
                return

            user_to_delete = next((auth_user for auth_user in authorized_users
                                   if auth_user['id'] == user.id), None)

            if user_to_delete is None:
                await ctx.send(
                    f'Unable to Delete: {user.display_name} does not exist authorized users', hidden=True
                )
                return

            authorized_users.remove(user_to_delete)
            set_value('authorized_users', authorized_users)
            await ctx.send(f'Removed {user.display_name} from authorized users', hidden=True
                           )
            return

        await ctx.send(
            'Error during authorized users change. Please check your inputs.', hidden=True)

    @cog_ext.cog_slash(name='botListAuthUsers', description='View authorized users for this bot', guild_ids=guild_ids)
    async def _bot_list_Auth_Users(self, ctx: SlashContext):
        author_id = str(ctx.author.id)
        authorized_users: list = get_value('authorized_users')
        await ctx.defer(hidden=True)

        # Check if authorized
        if next(
            (auth_user
             for auth_user in authorized_users if auth_user['id'] == author_id),
                None) is None:
            await ctx.send('Unauthorized to change authorized users', hidden=True)
            return

        user_string = ''
        for user in authorized_users:
            user_string += f"{user['name']}#{user['discriminator']}\n"
        await ctx.send(content=user_string, hidden=True)

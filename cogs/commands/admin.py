import discord
from discord.guild import Guild
from discord.member import Member
from discord.role import Role
from discord.user import User
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

    @cog_ext.cog_subcommand(base='admin', name='list_auth_users', description='View authorized users for this bot', guild_ids=guild_ids)
    async def _bot_list_Auth_Users(self, ctx: SlashContext) -> None:
        author_id = str(ctx.author.id)
        authorized_users: list = get_value('authorized_users')
        await ctx.defer(hidden=True)

        # Check if authorized
        if self._check_auth(author_id, authorized_users) is False:
            await ctx.send('Unauthorized to change authorized users', hidden=True)
            return

        user_string = ''
        for user in authorized_users:
            user_string += f"{user['name']}#{user['discriminator']}\n"
        await ctx.send(content=user_string, hidden=True)

    @cog_ext.cog_subcommand(base='admin', name='modify_auth_user',
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
                                     user: discord.User) -> None:
        author_id = str(ctx.author.id)
        authorized_users: list = get_value('authorized_users')
        print(author_id)
        print(authorized_users)
        await ctx.defer(hidden=True)

        # Check if authorized
        if self._check_auth(author_id, authorized_users) is False:
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

    @cog_ext.cog_subcommand(base='admin', name='setup_member', description='HC command to setup member',
                            guild_ids=guild_ids,
                            options=[
                                create_option(
                                    name='user', description='discord user to change', option_type=6, required=True),
                                create_option(
                                    name='name', description='name to change to - WITHOUT CMDR', option_type=3, required=True),
                                create_option(name='platform',
                                              description="platform the user plays on",
                                              option_type=3,
                                              required=True,
                                              choices=[
                                                  create_choice(
                                                      value='PC', name='PC'),
                                                  create_choice(value='Xbox One',
                                                                name='Xbox'),
                                                  create_choice(
                                                      value='Playstation 4', name='PS4'),
                                              ]),
                            ])
    async def _admin_setup_cmdr(self, ctx: SlashContext, user: Member, name: str, platform: str) -> None:
        author_id = str(ctx.author.id)
        # await ctx.defer(hidden=True)

        if self._check_auth(author_id) is False:
            await ctx.send('Unauthorized to perform setup of member', hidden=True)

        # nickname
        await user.edit(nick=f"CMDR {name}")

        # roles - remove New Member and Disassociate, add Fleet Member and cadet
        guild: Guild = ctx.guild
        member_role: Role = discord.utils.get(guild.roles, name='Fleet Member')
        cadet_role: Role = discord.utils.get(guild.roles, name='Cadet')
        new_role: Role = discord.utils.get(guild.roles, name='New Member')
        disassociate_role: Role = discord.utils.get(
            guild.roles, name='Dissociate Member')
        platform_role: Role = discord.utils.get(guild.roles, name=platform)

        await user.add_roles(member_role, reason="Cmdr Setup")
        await user.add_roles(cadet_role, reason="Cmdr Setup")
        await user.add_roles(platform_role, reason="Cmdr Setup")
        await user.remove_roles(new_role, reason='Cmdr Setup')
        await user.remove_roles(disassociate_role, reason='Cmdr Setup')

        await ctx.send(content='Member setup complete. Ready for Fleet Member ping.', hidden=True)

""" Handles commands for the Discord bot """
from datetime import datetime

import discord
from discord.ext.commands.bot import Bot
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

from mongo import get_value, set_value
import requests
import os
import json
from ranks import ranks

inara_api_url = 'https://inara.cz/inapi/v1/'


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

    @slash.slash(name='cmdr',
                 description="gives a description of the cmdr from inara",
                 guild_ids=test_guild_ids,
                 options=[create_option(name='cmdr', description="cmdr name", option_type=3, required=True)])
    async def _cmdr(ctx: SlashContext, cmdr_name: str):
        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        await ctx.defer()

        api_key = os.getenv('INARA_TOKEN', '')

        request_header = {'appName': 'USC Bot', 'appVersion': '1.0.0',
                          'isBeingDeveloped': 'true', 'APIkey': api_key}
        request_event = [{'eventName': 'getCommanderProfile',
                          'eventTimestamp': current_time, 'eventData': {'searchName': cmdr_name}}]
        data = {'header': request_header, 'events': request_event}
        json_data = json.dumps(data)
        response = requests.post(
            inara_api_url, data=json_data).json()

        response_code: int = response['events'][0]['eventStatus']

        if response_code == 204:
            await ctx.send("No inara profiles were found")
            return
        if response_code == 400:
            await ctx.send("There was an error executing that command")
            return

        try:

            cmdr_info = response['events'][0]['eventData']
            cmdr_ranks = cmdr_info['commanderRanksPilot']
            embed = discord.Embed(
                title='Inara Profile', url=cmdr_info['inaraURL'], description=f"Role: {cmdr_info.get('preferredGameRole', 'N/A')}")
            embed.set_author(name=cmdr_info['commanderName'],
                             url=cmdr_info['inaraURL'])
            if 'avatarImageURL' in cmdr_info:
                embed.set_thumbnail(url=cmdr_info['avatarImageURL'])
            for cmdr_rank in cmdr_ranks:
                rank_name: str = cmdr_rank['rankName']
                rank_value: int = int(cmdr_rank['rankValue'])
                rank_value_s: str = ranks[rank_name][rank_value]
                rank_progress = '' if rank_value_s == 'Elite' or rank_value_s == 'King' or rank_value_s == 'Admiral' else f"- {int(float(cmdr_rank['rankProgress']) *100)} %"
                embed.add_field(name=f"{rank_name.capitalize()} Rank",
                                value=f"{rank_value_s} {rank_progress}")

            if 'commanderSquadron' in cmdr_info:
                squad_info = cmdr_info['commanderSquadron']
                embed.add_field(
                    name="Squadron", value=f"{squad_info['squadronName']} - {squad_info['inaraURL']}", inline=False)

            embed.set_footer(
                text=f"Retrieved from Inara at the behest of {ctx.author.display_name}")
            await ctx.send(embed=embed)
        except discord.errors.NotFound:
            print('there was an error with the discord system')

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

import re

import requests
from discord import Embed, TextChannel
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
from mongo import get_value, set_value

GALNET_API = 'https://elitedangerous-website-backend-production.elitedangerous.com/api/galnet?_format=json'


class GalNet(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        print("Load Galnet Cog")
        self.watch_galnet.start()

    def cog_unload(self):
        self.watch_galnet.cancel()

    @tasks.loop(minutes=10.0)
    async def watch_galnet(self):
        data = await self.get_new_articles()
        if data:
            if len(data['articles']) > 0:
                channels_to_ping: list[str] = get_value('galnetChannels')

                for channel_to_ping in channels_to_ping:
                    channel: TextChannel = self.bot.get_channel(
                        int(channel_to_ping))

                    for article in data['articles']:
                        embed = Embed(
                            title=article['title'], description=article['body'])
                        embed.set_footer(text=article['date'])
                        await channel.send(embed=embed)

                id = data['articles'][0]['id']
                set_value('latestGalNet', id)
            else:
                print('No further articles')
        else:
            print('No further articles')

    @watch_galnet.before_loop
    async def before_watch(self):
        print('waiting to start watching galnet...')
        await self.bot.wait_until_ready()

    def process_data(self, data):
        updated_string = data['body']
        updated_string = re.sub('<p>', '', updated_string)
        updated_string = re.sub('<br \/>', '', updated_string)
        updated_string = re.sub('</p>', '', updated_string)
        updated_string = re.sub('\n$', '', updated_string)
        updated_string = re.sub('\n', '\n> ', updated_string)
        nid = int(data['nid'])

        data['body'] = updated_string
        data['id'] = nid
        return data

    async def get_new_articles(self):
        unprocessed_data = requests.get(GALNET_API).json()
        latest_id = get_value('latestGalNet')

        processed_data = map(self.process_data, unprocessed_data)

        if latest_id:
            new_articles = list(filter(
                lambda x: x['id'] > latest_id, processed_data))
            return {'articles': new_articles, 'current_id': latest_id}

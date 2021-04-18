import asyncio
import logging

import websocket
from discord import Embed, TextChannel
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
from mongo import get_value, set_value

logging.basicConfig(level=logging.INFO)

TICK_SOCKET = 'http://tick.phelbore.com:31173'


class BGSCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        print("Load BGS Cog")
        self.wsapp = websocket.WebSocketApp(
            TICK_SOCKET, on_message=self.on_message)

    def cog_unload(self):
        self.wsapp.close()

    async def on_message(self, wsapp, message):
        channel: TextChannel = self.bot.get_channel(831261490258509935)
        await channel.send(message)
        print(message)

    def log_message(self, message: str):
        logging.info(f"Message: {message}")

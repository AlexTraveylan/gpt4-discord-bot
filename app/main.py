from interactions import Client, Intents, listen

from app.core.constants import DISCORD_BOT_TOKEN
from app.core.logger.logger import LOGGER

bot = Client(intents=Intents.ALL)


@listen()
async def on_ready():
    LOGGER.info("Bot is ready!")


bot.start(DISCORD_BOT_TOKEN)

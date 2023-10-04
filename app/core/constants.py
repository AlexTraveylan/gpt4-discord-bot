from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
DISCORD_CLIENT_ID = int(os.environ["DISCORD_CLIENT_ID"])
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# give a delay for the bot to respond so it can catch multiple messages
SECONDS_DELAY_RECEIVING_MSG = 3
MAX_THREAD_MESSAGES = 200
MAX_CHARS_PER_REPLY_MSG = 1500
# text-davinci-003, gpt-3.5-turbo, gpt-4
MODEL = "gpt-3.5-turbo"

MAX_TOKENS = 2048

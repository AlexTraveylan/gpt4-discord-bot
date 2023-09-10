import logging


LOGGER = logging.getLogger("gt4-discord-bot-logger")
logging.basicConfig(
    format="[%(asctime)s] [%(filename)s:%(lineno)d] %(message)s", level=logging.INFO
)

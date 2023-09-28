from app.core.completion.base import ConversionState, Pmessage
from interactions import (
    Client,
    Intents,
    listen,
    slash_command,
    SlashContext,
    slash_option,
    Embed,
    BrandColors,
    OptionType,
)
from interactions.api.events.discord import MessageCreate
from app.core.completion.completion import generate_completion_response

from app.core.constants import DISCORD_BOT_TOKEN
from app.core.logger.logger import LOGGER

bot = Client(intents=Intents.ALL)


state = ConversionState()


@listen()
async def on_ready():
    LOGGER.info("Bot is ready!")


@slash_command(name="chat", description="Chat with Abra")
@slash_option(
    name="message_content",
    description="Your message",
    opt_type=OptionType.STRING,
    required=True,
)
async def chat(ctx: SlashContext, message_content: str):
    await ctx.defer()

    try:
        user_name = ctx.author.display_name
        user_id = ctx.author_id
        LOGGER.info(f"New chat request from {user_id} : {message_content[:20]}")

        state.reset()
        state.conversation.add_message(Pmessage("user", message_content))

        message = await ctx.send("Starting chat...")
        thread = await message.create_thread(name=f"Abra - {user_name}")
        state.conversation.thread = thread

        response = generate_completion_response(state)
        state.conversation.add_message(Pmessage("assistant", response.reply_text))

        await thread.send(response.reply_text)

    except Exception as e:
        LOGGER.error(str(e))
        await ctx.send(f"Failed to start chat {str(e)}", ephemeral=True)


@slash_command(name="stop", description="Stop chatting")
async def stop(ctx: SlashContext):
    await ctx.defer()
    state.stop()
    embed = Embed(description="Chat stopped", color=BrandColors.RED)

    await ctx.send(embed=embed)


@listen()
async def on_message_create(ctx: MessageCreate):
    if ctx.message._author_id == bot.user.id:
        return

    if not state.is_on:
        return

    if ctx.message.channel.id != state.conversation.thread.id:
        return

    state.conversation.add_message(Pmessage("user", ctx.message.content))

    response = generate_completion_response(state)
    state.conversation.add_message(Pmessage("assistant", response.reply_text))

    await state.conversation.thread.send(response.reply_text)


bot.start(DISCORD_BOT_TOKEN)

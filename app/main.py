from app.core.completion.base import ConversionState, Pmessage, SplitTooLongMessage
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

from app.core.constants import BOT_NAME, DISCORD_BOT_TOKEN, MAX_CHARS_PER_REPLY_MSG
from app.core.logger.logger import LOGGER

bot = Client(intents=Intents.ALL)


state = ConversionState()


@listen()
async def on_ready():
    LOGGER.info("Bot is ready!")


@slash_command(name="chat", description=f"Chat with {BOT_NAME}")
async def chat(ctx: SlashContext):
    await ctx.defer()

    try:
        user_name = ctx.author.display_name
        state.reset()
        message = await ctx.send("Starting chat...")
        thread = await message.create_thread(name=f"{BOT_NAME} - {user_name}")
        state.conversation.thread = thread

        await thread.send(f"Je suis {BOT_NAME}, un bot de discussion, expert en Python et TypeScript. Que puis-je faire pour toi ?")

    except Exception as e:
        LOGGER.error(str(e))
        await ctx.send(f"Failed to start chat : {str(e)}", ephemeral=True)


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
    state.conversation.current_total_tokens = response.total_tokens
    state.conversation.add_message(Pmessage("assistant", response.reply_text))

    embed = Embed(
        description=f"Tokens utilisés pour ce message : {state.conversation.current_total_tokens}",
        color=BrandColors.GREEN,
    )

    await state.conversation.thread.send(embed=embed)

    splited_messages = SplitTooLongMessage(response.reply_text).result()
    for message in splited_messages:
        await state.conversation.thread.send(message)


bot.start(DISCORD_BOT_TOKEN)

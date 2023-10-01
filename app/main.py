from app.core.completion.base import ConversionState, Pmessage, SplitTooLongMessage
from interactions import (
    TYPE_THREAD_CHANNEL,
    Client,
    Intents,
    SlashCommandChoice,
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

from app.core.constants import BOT_NAME, DISCORD_BOT_TOKEN
from app.core.logger.logger import LOGGER
from app.core.personnalities import factory_personality

bot = Client(intents=Intents.ALL)


state = ConversionState()


@listen()
async def on_ready():
    LOGGER.info("Bot is ready!")


@slash_command(name="chat", description=f"Chat with {BOT_NAME}")
@slash_option(
    name="personality",
    description="Personality to use",
    required=True,
    opt_type=OptionType.INTEGER,
    choices=[
        SlashCommandChoice("JakePy", 0),
        SlashCommandChoice("LilyLinux", 1),
        SlashCommandChoice("AvaFront", 2),
        SlashCommandChoice("Sam", 3),
    ],
)
async def chat(ctx: SlashContext, personality: int):
    await ctx.defer()

    if isinstance(ctx.channel, TYPE_THREAD_CHANNEL):
        embed = Embed(description="You can't chat in a thread", color=BrandColors.RED)
        return await ctx.send(embed=embed, ephemeral=True)

    bot_chosen = factory_personality(personality)
    state.conversation.set_bot_personnality(bot_chosen)

    try:
        user_name = ctx.author.display_name
        state.reset()
        message = await ctx.send(f"Début d'une conversation avec {bot_chosen.name}...")
        thread = await message.create_thread(name=f"{bot_chosen.name} - {user_name}")
        state.conversation.thread = thread

        embed = Embed(description=f"Je suis {bot_chosen.name}. {bot_chosen.description}", color=BrandColors.GREEN)

        await thread.send(embed=embed)

    except Exception as e:
        LOGGER.error(str(e))
        embed = Embed(description=f"Failed to start chat : {str(e)}", color=BrandColors.RED)
        await ctx.send(embed=embed, ephemeral=True)


@slash_command(name="stop", description="Stop chatting")
async def stop(ctx: SlashContext):
    await ctx.defer()
    state.stop()
    embed = Embed(description="Fin de la conversation", color=BrandColors.RED)

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

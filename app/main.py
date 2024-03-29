"""
Main file of the bot, it contains all the interactions with discord.
"""
from interactions import (
    TYPE_THREAD_CHANNEL,
    Client,
    EmbedAttachment,
    Intents,
    SlashCommandChoice,
    Task,
    TimeTrigger,
    listen,
    slash_command,
    SlashContext,
    slash_option,
    Embed,
    BrandColors,
    OptionType,
)

from interactions.api.events.discord import MessageCreate
import requests
from app.core.completion.completion import generate_completion_response
from app.core.completion.base import (
    ConversionState,
    Pmessage,
    SplitTooLongMessage,
)
from app.core.constants import Parameters
from app.core.create_image.base import factory_size
from app.core.create_image.create import create_image
from app.core.logger.logger import LOGGER
from app.core.personnalities import factory_personality

bot = Client(intents=Intents.ALL)


state = ConversionState()


@listen()
async def on_ready():
    """Listen to ready event."""
    LOGGER.info("Bot is ready!")


@slash_command(name="start_tasks", description="Start the tasks")
async def start_tasks(ctx: SlashContext):
    """Start the tasks."""
    begin_day.start()

    await ctx.send("Tasks started")


@slash_command(name="stop_tasks", description="Start the tasks")
async def stop_tasks(ctx: SlashContext):
    """Stop the tasks."""
    begin_day.stop()

    await ctx.send("Tasks ended")


@Task.create(TimeTrigger(hour=22, minute=59))
async def begin_day():
    """Cron job to create a new exercice every day."""
    body = {"admin_password": Parameters.ADMIN_SECRET}
    url = "https://alextraveylan.pythonanywhere.com/create_new_exercice"

    response = requests.post(url, json=body, timeout=500)

    channel = bot.get_channel(Parameters.MAIN_CHANNEL_ID)

    await channel.send(response.text)


@slash_command(name="generate_image", description="Use DALL-E to generate an image")
@slash_option(
    name="prompt",
    description="Text to generate image from",
    required=True,
    opt_type=OptionType.STRING,
)
@slash_option(
    name="nb_images",
    description="The number of images to generate",
    required=False,
    opt_type=OptionType.INTEGER,
)
@slash_option(
    name="size",
    description="The size of the image to generate",
    required=False,
    opt_type=OptionType.INTEGER,
    choices=[
        SlashCommandChoice("256x256", 0),
        SlashCommandChoice("512x512", 1),
        SlashCommandChoice("1024x1024", 2),
        SlashCommandChoice("1792x1024", 3),
        SlashCommandChoice("1024x1792", 4),
    ],
)
@slash_option(
    name="style",
    description="The style of the image to generate",
    required=False,
    opt_type=OptionType.INTEGER,
    choices=[SlashCommandChoice("vivid", 0), SlashCommandChoice("natural", 1)],
)
async def generate_image(
    ctx: SlashContext,
    prompt: str,
    nb_images: int = 1,
    size: int = 2,
    style: int = 0,
):
    """Generate an image from a prompt."""
    await ctx.defer()

    if ctx.author_id != Parameters.DISCORD_CLIENT_ID:
        return

    if isinstance(ctx.channel, TYPE_THREAD_CHANNEL):
        embed = Embed(description="You can't chat in a thread", color=BrandColors.RED)
        return await ctx.send(embed=embed, ephemeral=True)

    selected_size = factory_size(size)
    style = "vivid" if style == 0 else "natural"
    images = create_image(prompt, nb_images, selected_size, style)
    if len(images) > 0:
        images_urls = [EmbedAttachment(url=img_url) for img_url in images]

        # url is needed but its a bug, its can be patch anytime.
        embed = Embed(
            title=f"Images demandées par {ctx.user.tag}",
            description=prompt,
            color=BrandColors.GREEN,
            url="https://whatever.com",
            images=images_urls,
        )

        await ctx.send(embed=embed)
    else:
        embed = Embed(
            description="Failed to generate image",
            color=BrandColors.RED,
        )
        await ctx.send(embed=embed, ephemeral=True)


@slash_command(name="chat", description="Chat with a specific bot")
@slash_option(
    name="personality",
    description="Personality to use",
    required=False,
    opt_type=OptionType.INTEGER,
    choices=[
        SlashCommandChoice("JakePy", 0),
        SlashCommandChoice("LilyLinux", 1),
        SlashCommandChoice("AvaFront", 2),
        SlashCommandChoice("Sam", 3),
    ],
)
async def chat(ctx: SlashContext, personality: int = 3):
    """Start a conversation with a bot."""
    await ctx.defer()

    if ctx.author_id != Parameters.DISCORD_CLIENT_ID:
        return

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

        embed = Embed(
            description=f"Je suis {bot_chosen.name}. {bot_chosen.description}",
            color=BrandColors.GREEN,
        )

        await thread.send(embed=embed)

    except RuntimeError as e:
        LOGGER.error(str(e))
        embed = Embed(
            description=f"Failed to start chat: {str(e)}",
            color=BrandColors.RED,
        )
        await ctx.send(embed=embed, ephemeral=True)


@slash_command(name="stop_chat", description="Stop chatting")
async def stop(ctx: SlashContext):
    """Stop the conversation."""
    await ctx.defer()

    if ctx.author_id != Parameters.DISCORD_CLIENT_ID:
        return

    state.stop()
    embed = Embed(description="Fin de la conversation", color=BrandColors.RED)

    await ctx.send(embed=embed)


@slash_command(name="reset_chat", description="Reset the conversation state")
async def reset(ctx: SlashContext):
    """Reset the conversation."""
    await ctx.defer()

    if ctx.author_id != Parameters.DISCORD_CLIENT_ID:
        return

    state.conversation.reset_messages()
    embed = Embed(description="Conversation réinitialisée", color=BrandColors.GREEN)

    await ctx.send(embed=embed)


@listen()
async def on_message_create(ctx: MessageCreate):
    """Listen to message create event."""
    if ctx.message.author.id != Parameters.DISCORD_CLIENT_ID:
        return

    if ctx.message.author.id == bot.user.id:
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


bot.start(Parameters.DISCORD_BOT_TOKEN)

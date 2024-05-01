from enum import Enum

import discord
from discord import Interaction, app_commands, Embed

from discord.ext import commands
from loguru import logger

from commands import Voiceover
from config import env

intents = discord.Intents.default()
intents.message_content = False
CHARACTERS = [c.voice_name for c in env.VOICES]

assert len(CHARACTERS) > 0, "No voices found"

logger.info(f"Characters: {CHARACTERS}")
CharacterEnum = Enum("CharacterEnum", {c: c for c in CHARACTERS})


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
        )

    async def on_ready(self) -> None:
        logger.info(f"Loaded commands slash...")
        await self.tree.sync()

    async def setup_hook(self) -> None:
        logger.info(f"Logged in as {self.user.name}")


bot = Bot()


@bot.tree.command(
    name="talk",
    description="Talk to the bot",
)
@app_commands.checks.cooldown(1, 60.0, key=lambda i: (i.guild_id, i.user.id))
async def talk(interaction: Interaction, character: CharacterEnum, text: str) -> None:
    if len(text) > 100:
        raise ValueError("Text is too long, max 100 characters")

    await interaction.response.defer(ephemeral=False)  # type: ignore

    voiceover = Voiceover()
    try:
        await voiceover.speak(interaction, character.value, text)
    except Exception as e:
        logger.error(f"Error: {e}")
        await interaction.edit_original_response(content="An error occurred")


@talk.error
async def talk_error(interaction: Interaction, error: Exception) -> None:
    logger.error(f"Error: {error}")
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(  # noqa
            embed=Embed(
                title="❌ Cooldown!",
                description=f"Command on cooldown, try again in {error.retry_after:.0f} seconds",
                color=0xE02B2B
            ),
            ephemeral=True
        )
        return
    else:
        await interaction.edit_original_response(content=f"An error occurred: {error}")

if __name__ == "__main__":
    bot.run(env.DISCORD_TOKEN)

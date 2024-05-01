from enum import Enum

import discord
from discord import Interaction

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
async def talk(interaction: Interaction, character: CharacterEnum, text: str) -> None:
    await interaction.response.defer(ephemeral=False)  # type: ignore

    voiceover = Voiceover()
    try:
        await voiceover.speak(interaction, character.value, text)
    except Exception as e:
        logger.error(f"Error: {e}")
        await interaction.edit_original_response(content="An error occurred")


if __name__ == "__main__":
    bot.run(env.DISCORD_TOKEN)

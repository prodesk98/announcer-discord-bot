from typing import Literal

import discord
from discord import Interaction

from discord.ext import commands
from loguru import logger
from commands import Voiceover
from config import env

intents = discord.Intents.default()
intents.message_content = False


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
async def talk(interaction: Interaction, character: Literal["Hanzo", "Yuki"] = "Hanzo") -> None:
    await interaction.response.defer(ephemeral=False)  # type: ignore

    voiceover = Voiceover()
    await voiceover.speak(interaction, character)


if __name__ == "__main__":
    bot.run(env.DISCORD_TOKEN)

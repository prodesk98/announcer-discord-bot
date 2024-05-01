from pydantic import Field

from discord import Interaction


class Voiceover:
    def __init__(self):
        ...

    async def speak(self, interaction: Interaction, text: str = Field(..., max_length=360)) -> None:
        print(f"Speaking {text}")

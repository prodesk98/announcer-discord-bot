from typing import AsyncIterator

import httpx
from elevenlabs import VoiceSettings, Voice
from pydantic import Field

from discord import Interaction

from elevenlabs.client import AsyncElevenLabs
from elevenlabs import stream

from config import env
from models import CharacterModel

client_elevenlabs = AsyncElevenLabs(
    api_key=env.ELEVENLABS_TOKEN,
    httpx_client=httpx.AsyncClient()
)


def _search_voice(c: str) -> CharacterModel:
    for voice in env.VOICES:
        if voice.voice_name == c:
            return voice
    raise ValueError(f"Voice {c} not found")


class Voiceover:
    @staticmethod
    async def generate_voice(character: CharacterModel, text: str) -> bytes:
        audio = await client_elevenlabs.generate(
            text=text,
            voice=Voice(
                voice_id=character.voice_id,
                settings=VoiceSettings(stability=0.5, similarity_boost=0.75, style=0.0, use_speaker_boost=True)
            )
        )
        return stream(audio)  # type: ignore

    async def speak(self, interaction: Interaction, char: str, text: str = Field(..., max_length=360)) -> None:
        audio = await self.generate_voice(_search_voice(char), text)
        print(audio)
        await interaction.edit_original_response(content="**playing voice**: " + text)

from asyncio import to_thread
from elevenlabs import VoiceSettings, Voice
from pydantic import Field

from discord import Interaction

from elevenlabs.client import ElevenLabs

from tempfile import NamedTemporaryFile

from config import env
from utils import PlayAudio

client_eleven_labs = ElevenLabs(api_key=env.ELEVENLABS_TOKEN)


def _search_voice(c: str) -> str:
    for voice in env.VOICES:
        if voice.voice_name == c:
            return voice.voice_id
    raise ValueError(f"Voice {c} not found")


class Voiceover:
    @staticmethod
    def _generate(text: str, voice: Voice) -> bytes:
        audio_stream = client_eleven_labs.generate(text=text, voice=voice, stream=True, model="eleven_multilingual_v2")
        audio_bytes = b""
        for chunk in audio_stream:
            if chunk is not None:
                audio_bytes += chunk
        return audio_bytes

    @staticmethod
    async def generate_voice(voice_id: str, text: str) -> bytes:
        return await to_thread(
            Voiceover._generate,
            text=text,
            voice=Voice(
                voice_id=voice_id,
                settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.75,
                    style=0.0,
                    use_speaker_boost=True,
                ),
            )
        )

    async def speak(self, interaction: Interaction, char: str, text: str = Field(..., max_length=75)) -> None:
        audio = await self.generate_voice(_search_voice(char), text)
        tmp_audio = NamedTemporaryFile(delete=True, suffix=".mp3")
        tmp_audio.write(audio)
        tmp_audio.seek(0)
        await PlayAudio(interaction, tmp_audio.name)
        await interaction.edit_original_response(content=f"**playing voice**: {text}")

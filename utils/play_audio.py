import asyncio
from os import PathLike

from discord import Interaction, VoiceState, VoiceClient, utils as discord_utils, FFmpegOpusAudio


async def PlayAudio(interaction: Interaction, audio_path: str | PathLike) -> None:
    if interaction.user.voice is None:
        await interaction.edit_original_response(content="You must be in a voice channel")
        return

    voice: VoiceState | VoiceClient = discord_utils.get(interaction.client.voice_clients, guild=interaction.user.guild)  # type: ignore
    if voice is None:
        voice = await interaction.user.voice.channel.connect()
    elif voice.channel != interaction.user.voice.channel:
        await voice.move_to(interaction.user.voice.channel)
        await asyncio.sleep(3)

    source = FFmpegOpusAudio(
        executable="ffmpeg",
        source=audio_path,
        **{'options': '-vn -af "volume=20dB"'}
    )
    if voice.is_playing():
        voice.stop()
    voice.play(source)

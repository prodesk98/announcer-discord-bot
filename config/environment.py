from pydantic import BaseModel
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Environment(BaseModel):
    DISCORD_TOKEN: str = getenv("DISCORD_TOKEN")
    ELEVENLABS_TOKEN: str = getenv("ELEVENS_TOKEN")
    ELEVENLABS_VOICE_ID: str = getenv("VOICE_ID")

    # valid
    if not DISCORD_TOKEN:
        raise ValueError("DISCORD_TOKEN is not set")
    if not ELEVENLABS_TOKEN:
        raise ValueError("ELEVENLABS_TOKEN is not set")
    if not ELEVENLABS_VOICE_ID:
        raise ValueError("ELEVENLABS_VOICE_ID is not set")


env = Environment()

from typing import List

from pydantic import BaseModel
from os import getenv
from dotenv import load_dotenv
from orjson import loads

from models import CharacterModel

load_dotenv()


def _get_voices_config() -> List[CharacterModel]:
    with open("config/voices.json") as f:
        return [CharacterModel(**voice) for voice in loads(f.read())]


class Environment(BaseModel):
    DISCORD_TOKEN: str = getenv("DISCORD_TOKEN")
    ELEVENLABS_TOKEN: str = getenv("ELEVENLABS_TOKEN")
    VOICES: List[CharacterModel] = _get_voices_config()

    # valid
    if not DISCORD_TOKEN:
        raise ValueError("DISCORD_TOKEN is not set")
    if not ELEVENLABS_TOKEN:
        raise ValueError("ELEVENLABS_TOKEN is not set")
    if not VOICES:
        raise ValueError("VOICES is not set")


env = Environment()

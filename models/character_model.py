from pydantic import BaseModel


class CharacterModel(BaseModel):
    voice_id: str
    voice_name: str

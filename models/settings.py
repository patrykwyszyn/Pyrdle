from pydantic import BaseModel


class Settings(BaseModel):
    language: str
    easy_mode_filename: str
    medium_mode_filename: str
    hard_mode_filename: str
    alphabet: str


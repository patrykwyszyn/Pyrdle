import csv
import json
import os
from typing import Dict

from models.difficulty import Difficulty
from models.settings import Settings


class FileReader:
    alphabet: str = "QWERTYUIOPASDFGHJKLZXCVBNM"
    language_specific_letters: str

    def __init__(self, language: str):
        self.path = f"resources/{language}/"
        with open("config.json", encoding="utf8") as file:
            json_object = json.load(file)
            self.settings: Settings = Settings(**json_object[language])

        self.alphabet += self.settings.language_specific_letters
        self.language_specific_letters = self.settings.language_specific_letters

    def get_words(self, chosen_mode: Difficulty):
        paths: Dict[str, str] = {
            Difficulty.EASY: self.settings.easy_mode_filename,
            Difficulty.MEDIUM: self.settings.medium_mode_filename,
            Difficulty.HARD: self.settings.hard_mode_filename
        }

        return next(csv.reader(open(os.path.join(self.path, paths[chosen_mode]), encoding="utf8")))

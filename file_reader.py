import csv
import json
import os
from typing import List

from models.settings import Settings


class FileReader:
    easy_mode_words: List[str]
    medium_mode_words: List[str]
    hard_mode_words: List[str]
    alphabet: List[str]

    def __init__(self, language: str):
        path = f"resources/{language}/"
        with open("config.json") as file:
            json_object = json.load(file)
            settings: Settings = Settings(**json_object[language])
            self.easy_mode_words = next(csv.reader(open(os.path.join(path, settings.easy_mode_filename))))
            self.medium_mode_words = next(csv.reader(open(os.path.join(path, settings.medium_mode_filename))))
            self.hard_mode_words = next(csv.reader(open(os.path.join(path, settings.hard_mode_filename))))
            self.alphabet = list(settings.alphabet)

    def get_alphabet_in_parts(self):
        k, m = divmod(len(self.alphabet), 3)
        return list((self.alphabet[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(3)))



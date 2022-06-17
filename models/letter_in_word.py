from UI.letter import Letter


class LetterInWord:
    letter: Letter
    index: int

    def __init__(self, letter: Letter, index: int):
        self.letter = letter
        self.index = index

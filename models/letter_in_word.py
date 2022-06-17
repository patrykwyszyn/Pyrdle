from UI.letterbox import LetterBox


class LetterInWord:
    letter: LetterBox
    index: int

    def __init__(self, letter: LetterBox, index: int):
        self.letter = letter
        self.index = index

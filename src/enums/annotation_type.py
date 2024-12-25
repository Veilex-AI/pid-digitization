from enum import Enum

class AnnotationType(str, Enum):
    LINES = "lines"
    WORDS   = "words"
    SYMBOLS = "symbols"
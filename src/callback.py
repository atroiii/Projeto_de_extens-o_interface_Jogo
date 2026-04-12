"""Docs."""

from enum import IntEnum, auto


class Callback(IntEnum):
    QUESTION_LOADED = auto()
    BUZZER_ACTIVATED = auto()
    ANSWER_PROCESSED = auto()
    GAME_FINISHED = auto()

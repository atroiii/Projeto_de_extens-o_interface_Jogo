"""Docs."""

from settings import Settings
from tkinter import font as tkfont

import os
import platform


class QuizFont:
    """Docs."""

    title: tkfont.Font
    big: tkfont.Font
    median: tkfont.Font
    small: tkfont.Font
    choice: tkfont.Font
    buzzer: tkfont.Font

    @staticmethod
    def init() -> None:
        QuizFont.title = tkfont.Font(
            family=Settings.FONT_TITLE, size=Settings.FONT_TITLE_SIZE, weight="bold"
        )
        QuizFont.big = tkfont.Font(
            family=Settings.FONT_BASE, size=Settings.FONT_BIG_SIZE, weight="bold"
        )
        QuizFont.median = tkfont.Font(
            family=Settings.FONT_BASE, size=Settings.FONT_MEDIAN_SIZE
        )
        QuizFont.small = tkfont.Font(
            family=Settings.FONT_BASE, size=Settings.FONT_SMALL_SIZE
        )
        QuizFont.choice = tkfont.Font(
            family=Settings.FONT_BASE, size=Settings.FONT_CHOICE_SIZE, weight="bold"
        )
        QuizFont.buzzer = tkfont.Font(
            family=Settings.FONT_BASE, size=Settings.FONT_BUZZER_SIZE, weight="bold"
        )

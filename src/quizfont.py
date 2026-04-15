"""Docs."""

from settings import Settings
from tkinter import font as tkfont

from pathlib import Path
import os
import platform
import ctypes

from typing import Any, Optional

AddFontResourceExW: Any = None

if platform.system() == "Windows":
    from ctypes import wintypes

    try:
        gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)
        AddFontResourceExW = gdi32.AddFontResourceExW

        AddFontResourceExW.argtypes = [
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.LPVOID,
        ]
        AddFontResourceExW.restype = wintypes.INT

    except (AttributeError, OSError):
        AddFontResourceExW = None


def font_load(fontpath: Path) -> Optional[int]:
    assert fontpath.exists(), f"ERROR: File path {fontpath} does not exist."

    if platform.system() == "Windows" and AddFontResourceExW is not None:
        flags = 0x10
        return AddFontResourceExW(str(fontpath), flags, 0)

    return None


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
        if platform.system() == "Windows":
            font_load(Path("../res/fonts/PressStart2P-Regular.ttf"))
            fonts = tkfont.families()
            target_font = [font for font in fonts if "Press Start 2P" in font or "PressStart2P" in font]
            assert len(target_font) > 0, f"ERRO: Fonte nao encontrada no sistema. Disponiveis: {fonts[:5]}"
            Settings.FONT_TITLE = target_font[0]
            Settings.FONT_BASE = target_font[0]

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

"""Docs."""

from typing import TypeAlias, Literal

ReliefType: TypeAlias = Literal["raised", "sunken", "flat", "ridge", "solid", "groove"]


class Settings:
    TITLE: str = "Quiz "

    KEY_BUZZER_ACTIVATE_0: str = "<F1>"
    KEY_BUZZER_ACTIVATE_1: str = "<F2>"

    KEY_WINDOW_FULLSCREEN: str = "<F11>"
    KEY_WINDOW_MINIMIZE: str = "<Escape>"

    FONT_TITLE: str = "Impact"
    FONT_BASE: str = "JetBrains Mono" #"Comic Sans Ms"
    FONT_TITLE_SIZE: int = 42
    FONT_BIG_SIZE: int = 16
    FONT_MEDIAN_SIZE: int = 13
    FONT_SMALL_SIZE: int = 11
    FONT_CHOICE_SIZE: int = 13
    FONT_BUZZER_SIZE: int = 22

    COR_TEXTO: str = "black"
    COR_BOTAO: str = "#3498db"
    COR_CERTO: str = "#2ecc71"  # verde para resposta correta
    COR_ERRADO: str = "#e74c3c"  # vermelho para resposta errada
    FONTE_PADRAO: tuple[str, int] = ("Arial", 12)

    COR_CARD: str = "#FFFFFF"
    COR_HOVER: str = "#FFFFFF"
    COR_TITULO: str = "#FFFFFF"
    COR_OURO: str = "#FFFFFF"
    COR_BUZZER: str = "#FFFFFF"
    COR_P1: str = "#FFFFFF"
    COR_P2: str = "#FFFFFF"
    COR_BG: str = "#ecf0f1"

    class Button:
        RELIEF: ReliefType = "flat"
        CURSOR = "hand2"
        PADX: int = 10
        PADY: int = 6

    class Card:
        RELIEF: ReliefType = "flat"

    class Menu:
        TITLE: str = "TechQuiz"
        SUBTITLE: str = "10 perguntas | Quem errar passa a vez."

        PLAYER_1_ICON: str = "🔵"
        PLAYER_2_ICON: str = "🔴"

        ARDUINO_CONNECTION_MSG = "⚡ Conexão Arduino"

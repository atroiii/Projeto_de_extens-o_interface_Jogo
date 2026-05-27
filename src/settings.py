"""Docs."""

from typing import TypeAlias, Literal

ReliefType: TypeAlias = Literal["raised", "sunken", "flat", "ridge", "solid", "groove"]


class Settings:
    BAUD_RATE: int = 9600
    THREAD_DELAY: float = 0.1

    TITLE: str = "Quiz"

    KEY_BUZZER_ACTIVATE_0: str = "<F1>"
    KEY_BUZZER_ACTIVATE_1: str = "<F2>"

    KEY_WINDOW_FULLSCREEN: str = "<F11>"
    KEY_WINDOW_MINIMIZE: str = "<Escape>"

    FONT_TITLE: str = "PressStart2P"
    FONT_BASE: str = "PressStart2P"
    FONT_TITLE_SIZE: int = 2**5
    FONT_BIG_SIZE: int = 2**4
    FONT_MEDIAN_SIZE: int = 2**4
    FONT_SMALL_SIZE: int = 2**3
    FONT_CHOICE_SIZE: int = 2**3
    FONT_BUZZER_SIZE: int = 2**5

    COR_TEXTO: str = "black"
    COR_BOTAO: str = "#3498db"
    COR_CERTO: str = "#2ecc71"
    COR_ERRADO: str = "#e74c3c"
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
        ARDUINO_CONNECTION_MSG: str = "Conexão Arduino"
        BEGIN_BUTTON_MSG: str = " COMEÇAR "
        SCOREBOARD_BUTTON_MSG: str = "PLACAR DA SESSÃO"

    class History:
        WINDOW_TITLE: str = "Resultados da Sessão"
        WINDOW_RES: str = "450x500"
        TITLE: str = "RESULTADOS ATUAIS"
        NOGAMES_MSG: str = "Nenhum jogo finalizado nesta sessão."
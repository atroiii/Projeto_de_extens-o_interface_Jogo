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

    # Mude esse bloco no seu settings.py para iniciar com os tamanhos maiores:
    FONT_TITLE: str = "PressStart2P"
    FONT_BASE: str = "PressStart2P"
    FONT_TITLE_SIZE: int = 32   # Alterado de 2**5 (que dava 32, mas agora fixamos direto)
    FONT_BIG_SIZE: int = 16     # Alterado de 16
    FONT_MEDIAN_SIZE: int = 16  # Alterado de 16
    FONT_SMALL_SIZE: int = 12   # Alterado de 8
    FONT_CHOICE_SIZE: int = 14  # Alterado de 8
    FONT_BUZZER_SIZE: int = 32  # Alterado de 32

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
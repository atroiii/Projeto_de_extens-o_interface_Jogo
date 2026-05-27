"""Docs."""

from settings import Settings
from tkinter import messagebox
from tkinter import Tk
from themesdata import TEMAS


class Theme:
    current_index: int = 1

    @staticmethod
    def chance(root) -> None:
        """Docs."""

        Theme.current_index = (Theme.current_index + 1) % len(TEMAS)
        Theme.apply(root)
        root.update_menu()

    @staticmethod
    def apply(root: Tk) -> None:
        """Applica to tema
        Args:
            root (Tk): Uma instancia de QuizUI, e.g. Theme.apply(self)
        """
        tema = TEMAS[Theme.current_index]
        Settings.COR_CERTO = "#2ecc71"
        Settings.COR_ERRADO = "#e74c3c"

        Settings.COR_BG = tema["BG"]
        Settings.COR_CARD = tema["CARD"]
        Settings.COR_BOTAO = tema["BOTAO"]
        Settings.COR_HOVER = tema["HOVER"]
        Settings.COR_TEXTO = tema["TEXTO"]
        Settings.COR_TITULO = tema["TITULO"]
        Settings.COR_OURO = tema["OURO"]
        Settings.COR_BUZZER = tema["BUZZER"]
        Settings.COR_P1 = tema["P1"]
        Settings.COR_P2 = tema["P2"]

        root.configure(bg=Settings.COR_BG)

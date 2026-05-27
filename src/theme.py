"""Docs."""

from settings import Settings
from quizfont import QuizFont
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

class FontTheme:
    # 1. ATUALIZADO AQUI: Adicionamos os novos modos na lista para o botão saber que eles existem!
    font_modes = ["pixel", "comic", "moderna", "retro_mono"]
    current_index = 0

    @staticmethod
    def chance(root) -> None:
        # Avança para a próxima fonte da lista toda vez que clica no botão "Aa"
        FontTheme.current_index = (FontTheme.current_index + 1) % len(FontTheme.font_modes)
        modo = FontTheme.font_modes[FontTheme.current_index]

        if modo == "pixel":
            Settings.FONT_TITLE = "PressStart2P"
            Settings.FONT_BASE = "PressStart2P"
            Settings.FONT_TITLE_SIZE = 32
            Settings.FONT_BIG_SIZE = 16
            Settings.FONT_MEDIAN_SIZE = 16
            Settings.FONT_SMALL_SIZE = 12
            Settings.FONT_CHOICE_SIZE = 14
            Settings.FONT_BUZZER_SIZE = 32
            # Recarrega o mapeamento da fonte TTF caso esteja no Windows
            QuizFont.init()

        elif modo == "comic":
            Settings.FONT_TITLE = "Comic Sans MS"
            Settings.FONT_BASE = "Comic Sans MS"
            Settings.FONT_TITLE_SIZE = 24
            Settings.FONT_BIG_SIZE = 16
            Settings.FONT_MEDIAN_SIZE = 14
            Settings.FONT_SMALL_SIZE = 11
            Settings.FONT_CHOICE_SIZE = 12
            Settings.FONT_BUZZER_SIZE = 24

        # Seu trecho da fonte Arial adicionado perfeitamente aqui:
        elif modo == "moderna":
            Settings.FONT_TITLE = "Arial"
            Settings.FONT_BASE = "Arial"
            Settings.FONT_TITLE_SIZE = 26
            Settings.FONT_BIG_SIZE = 16
            Settings.FONT_MEDIAN_SIZE = 14
            Settings.FONT_SMALL_SIZE = 12
            Settings.FONT_CHOICE_SIZE = 13
            Settings.FONT_BUZZER_SIZE = 26

        # Seu trecho da fonte Courier New adicionado perfeitamente aqui:
        elif modo == "retro_mono":
            Settings.FONT_TITLE = "Courier New"
            Settings.FONT_BASE = "Courier New"
            Settings.FONT_TITLE_SIZE = 26
            Settings.FONT_BIG_SIZE = 16
            Settings.FONT_MEDIAN_SIZE = 14
            Settings.FONT_SMALL_SIZE = 12
            Settings.FONT_CHOICE_SIZE = 13
            Settings.FONT_BUZZER_SIZE = 26

        # Atualiza as fontes ativas no Tkinter com o tamanho e família escolhidos acima
        QuizFont.title.config(family=Settings.FONT_TITLE, size=Settings.FONT_TITLE_SIZE)
        QuizFont.big.config(family=Settings.FONT_BASE, size=Settings.FONT_BIG_SIZE)
        QuizFont.median.config(family=Settings.FONT_BASE, size=Settings.FONT_MEDIAN_SIZE)
        QuizFont.small.config(family=Settings.FONT_BASE, size=Settings.FONT_SMALL_SIZE)
        QuizFont.choice.config(family=Settings.FONT_BASE, size=Settings.FONT_CHOICE_SIZE)
        QuizFont.buzzer.config(family=Settings.FONT_BASE, size=Settings.FONT_BUZZER_SIZE)

        # Redesenha o menu com a nova fonte aplicada
        root.update_menu()
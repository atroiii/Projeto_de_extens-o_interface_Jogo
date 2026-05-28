import tkinter as tk
from random import choice
import os
from pathlib import Path


class QuizRes:
    theme_chance_icon = None
    reload_ports_icon = None
    player_1_icon = None
    player_2_icon = None
    ports_icon = None
    history_icon = None
    question_icon = None
    winner_icon = None
    try_again_ans_icon = None
    correct_ans_icon = None
    fail_ans = None
    
    # NOVA VARIÁVEL GLOBAL: Guardará a lista com todas as imagens carregadas
    lista_todos_avatares: list[tk.PhotoImage] = []

    IMG_SCALE: tuple[int, int] = (3, 3)

    @staticmethod
    def load_image(file: Path) -> tk.PhotoImage | None:
        if not file.exists():
            print(f"WARNING: Failed to load, {file}")
            return None

        return tk.PhotoImage(file=file).zoom(*QuizRes.IMG_SCALE)

    @staticmethod
    def init() -> bool:
        """Docs."""

        QuizRes.theme_chance_icon = QuizRes.load_image(
            file=Path("../res/tiles/tile_0151.png")
        )
        QuizRes.reload_ports_icon = QuizRes.load_image(
            file=Path("../res/tiles/tile_0209.png")
        )
        QuizRes.ports_icon = QuizRes.load_image(file=Path("../res/tiles/tile_0132.png"))
        QuizRes.history_icon = QuizRes.load_image(
            file=Path("../res/tiles/tile_0007.png")
        )
        QuizRes.question_icon = QuizRes.load_image(
            file=Path("../res/tiles/tile_0180.png")
        )
        QuizRes.winner_icon = QuizRes.load_image(file=Path("../res/tiles/tile_0107.png"))

        QuizRes.try_again_ans_icon = QuizRes.load_image(
            file=Path("../res/tiles/tile_0016.png")
        )
        QuizRes.correct_ans_icon = QuizRes.load_image(
            file=Path("../res/tiles/tile_0070.png")
        )
        QuizRes.fail_ans = QuizRes.load_image(file=Path("../res/tiles/tile_0122.png"))

        # =========================================================================
        # NOVA LÓGICA: CARREGANDO TODOS OS AVATARES DA PASTA CHAR
        # =========================================================================
        QuizRes.lista_todos_avatares = []
        pasta_char = Path("../res/char")
        
        if pasta_char.exists():
            # Filtra apenas por arquivos (evita ler subpastas escondidas do sistema)
            chars = [f for f in os.listdir(pasta_char) if os.path.isfile(pasta_char / f)]
            
            # Carrega cada um dos personagens encontrados e adiciona na lista
            for nome_arquivo in chars:
                img = QuizRes.load_image(file=pasta_char / nome_arquivo)
                if img:
                    QuizRes.lista_todos_avatares.append(img)

        # Fallback de segurança: Se a pasta estiver vazia, usa ícones padrão para o jogo não quebrar
        if not QuizRes.lista_todos_avatares:
            QuizRes.lista_todos_avatares = [QuizRes.question_icon, QuizRes.winner_icon]

        # Define quais serão os avatares iniciais (caso o jogador decida não apertar as setas)
        QuizRes.player_1_icon = QuizRes.lista_todos_avatares[0]
        QuizRes.player_2_icon = QuizRes.lista_todos_avatares[1] if len(QuizRes.lista_todos_avatares) > 1 else QuizRes.lista_todos_avatares[0]

        return True
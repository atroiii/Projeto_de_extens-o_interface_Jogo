"""Docs."""

import tkinter as tk
from random import choice
import os


class QuizRes:
    theme_chance_icon = None
    reload_ports_icon = None
    player_1_icon = None
    player_2_icon = None
    ports_icon = None
    history_icon = None
    question_icon = None

    @staticmethod
    def init() -> bool:
        """Docs."""

        IMG_SCALE: int = (3, 3)
        QuizRes.theme_chance_icon = tk.PhotoImage(
            file="./res/tiles/tile_0151.png"
        ).zoom(*IMG_SCALE)
        QuizRes.reload_ports_icon = tk.PhotoImage(
            file="./res/tiles/tile_0209.png"
        ).zoom(*IMG_SCALE)
        QuizRes.ports_icon = tk.PhotoImage(file="./res/tiles/tile_0132.png").zoom(
            *IMG_SCALE
        )
        QuizRes.history_icon = tk.PhotoImage(file="./res/tiles/tile_0007.png").zoom(
            *IMG_SCALE
        )
        QuizRes.question_icon = tk.PhotoImage(file="./res/tiles/tile_0180.png").zoom(
            *IMG_SCALE
        )
        QuizRes.winner_icon = tk.PhotoImage(file="./res/tiles/tile_0107.png").zoom(
            *IMG_SCALE
        )

        QuizRes.try_again_ans_icon = tk.PhotoImage(
            file="./res/tiles/tile_0016.png"
        ).zoom(*IMG_SCALE)
        QuizRes.correct_ans_icon = tk.PhotoImage(file="./res/tiles/tile_0070.png").zoom(
            *IMG_SCALE
        )
        QuizRes.fail_ans = tk.PhotoImage(file="./res/tiles/tile_0122.png").zoom(
            *IMG_SCALE
        )

        chars = os.listdir("./res/char")
        QuizRes.player_1_icon = tk.PhotoImage(file=f"./res/char/{choice(chars)}").zoom(
            *IMG_SCALE
        )
        QuizRes.player_2_icon = tk.PhotoImage(file=f"./res/char/{choice(chars)}").zoom(
            *IMG_SCALE
        )

        return True

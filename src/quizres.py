"""Docs."""

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
            file=Path("./res/tiles/tile_0151.png")
        )
        QuizRes.reload_ports_icon = QuizRes.load_image(
            file=Path("./res/tiles/tile_0209.png")
        )
        QuizRes.ports_icon = QuizRes.load_image(file=Path("./res/tiles/tile_0132.png"))
        QuizRes.history_icon = QuizRes.load_image(
            file=Path("./res/tiles/tile_0007.png")
        )
        QuizRes.question_icon = QuizRes.load_image(
            file=Path("./res/tiles/tile_0180.png")
        )
        QuizRes.winner_icon = QuizRes.load_image(file=Path("./res/tiles/tile_0107.png"))

        QuizRes.try_again_ans_icon = QuizRes.load_image(
            file=Path("./res/tiles/tile_0016.png")
        )
        QuizRes.correct_ans_icon = QuizRes.load_image(
            file=Path("./res/tiles/tile_0070.png")
        )
        QuizRes.fail_ans = QuizRes.load_image(file=Path("./res/tiles/tile_0122.png"))

        chars = os.listdir(Path("./res/char"))
        QuizRes.player_1_icon = QuizRes.load_image(
            file=Path(f"./res/char/{choice(chars)}")
        )
        QuizRes.player_2_icon = QuizRes.load_image(
            file=Path(f"./res/char/{choice(chars)}")
        )

        return True

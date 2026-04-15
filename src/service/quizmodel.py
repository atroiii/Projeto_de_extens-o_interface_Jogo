"""Docs."""

from typing import Any

from typing import Callable, Final
from callback import Callback

from tkinter import messagebox
from quizgame import QuizGame, Player

import random
import threading
import serial
import serial.tools.list_ports

from settings import Settings
from emulator import Emulator, gen_random_port_list

from service.dataset import PERGUNTAS, TOTAL_PERGUNTAS
from callback import Callback

from quizres import QuizRes
import time


class SerialManager:
    serial_conn = None
    running: bool = False
    callback_buzzer: Callable | None = None

    @staticmethod
    def init(callback_buzzer: Callable) -> bool:
        SerialManager.callback_buzzer = callback_buzzer
        return True

    @staticmethod
    def ports_list() -> list:
        if Settings.EMULATE_ARDUINO:
            return Emulator.ports_list(SerialManager)

        return [p.device for p in serial.tools.list_ports.comports()]

    @staticmethod
    def connect(port) -> bool:
        if Settings.EMULATE_ARDUINO:
            Emulator.connect(SerialManager, port)
            return True

        try:
            SerialManager.serial_conn = serial.Serial(
                port, Settings.BAUD_RATE, timeout=0.1
            )
            SerialManager.running = True
            threading.Thread(target=SerialManager.read, daemon=True).start()
            return True

        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return False

    @staticmethod
    def disconnect() -> Any:
        if Settings.EMULATE_ARDUINO:
            Emulator.disconnect(SerialManager)
            return

        SerialManager.running = False
        if not SerialManager.serial_conn:
            return
        try:
            SerialManager.serial_conn.close()

        except Exception:
            ...
        SerialManager.serial_conn = None

    @staticmethod
    def read() -> Any:
        if Settings.EMULATE_ARDUINO:
            Emulator.read(SerialManager)
            return

        # NOTE: Exceptions needs types
        while SerialManager.running and SerialManager.serial_conn is not None:
            try:
                if SerialManager.serial_conn.in_waiting:
                    linha = SerialManager.serial_conn.readline().decode("utf-8").strip()
                    if (
                        linha in ("1", "2")
                        and SerialManager.callback_buzzer is not None
                    ):
                        jogador = int(linha) - 1
                        SerialManager.callback_buzzer(jogador)
            except Exception:
                break
            time.sleep(Settings.THREAD_DELAY)

    @staticmethod
    def send(cmd: Any) -> Any:
        if Settings.EMULATE_ARDUINO:
            Emulator.send(SerialManager, cmd)
            return

        if SerialManager.serial_conn and SerialManager.serial_conn.is_open:
            try:
                SerialManager.serial_conn.write((cmd + "\n").encode())
            except Exception:
                pass


# NOTE: Para indexação dos pontos
PLAYER_1: Final[int] = 0
PLAYER_2: Final[int] = 1


class QuizModel:
    """Docs."""

    callbacks: dict[Callback, Callable | None] = {}
    session_history: list[QuizGame] = [
        QuizGame(Player("foo", 100), Player("baz", 200), winner=0)
    ]

    player_1_name: str = ""
    player_2_name: str = ""

    points: list[int] = [0, 0]

    questions: list = []

    q_index: int = 0

    current_player: int = 0

    first_try: bool = True
    is_answering: bool = False
    is_waiting_buzzer: bool = False

    class Question:
        @staticmethod
        def load() -> None:
            QuizModel.first_try = True
            QuizModel.is_waiting_buzzer = True
            QuizModel.is_answering = False

            q = QuizModel.questions[QuizModel.q_index]
            QuizModel.emit(
                Callback.QUESTION_LOADED,
                pergunta=q["pergunta"],
                opcoes=q["opcoes"],  # <-- agora as alternativas são enviadas
                numero=QuizModel.q_index + 1,
                total=TOTAL_PERGUNTAS,
                nome_p1=QuizModel.player_1_name,
                nome_p2=QuizModel.player_2_name,
                pontos_p1=QuizModel.points[PLAYER_1],
                pontos_p2=QuizModel.points[PLAYER_2],
            )

            SerialManager.send("READY")

        @staticmethod
        def next() -> None:
            QuizModel.q_index += 1

            if not (QuizModel.q_index >= TOTAL_PERGUNTAS):
                QuizModel.Question.load()
                return

            QuizModel.register_end_of_game()
            QuizModel.emit(
                Callback.GAME_FINISHED,
                nome_p1=QuizModel.player_1_name,
                nome_p2=QuizModel.player_2_name,
                pontos_p1=QuizModel.points[PLAYER_1],
                pontos_p2=QuizModel.points[PLAYER_2],
            )

    @staticmethod
    def init(player_1_name: str, player_2_name: str, port) -> None:
        """Docs."""

        QuizModel.player_1_name = player_1_name
        QuizModel.player_2_name = player_2_name
        QuizModel.points = [0, 0]
        QuizModel.questions = random.sample(PERGUNTAS, TOTAL_PERGUNTAS)
        QuizModel.q_index = 0

        SerialManager.callback_buzzer = QuizModel.on_buzzer
        if port:
            SerialManager.connect(port)

        QuizModel.Question.load()

    @staticmethod
    def buzzer_activate(player) -> None:
        """Docs."""

        messagebox.showwarning("Error", "Não implementado")
        raise NotImplementedError("ERROR: buzzer_activate")

    @staticmethod
    def register_callback(event: Callback, func: Callable) -> None:
        """Docs."""

        assert event not in QuizModel.callbacks, "ERROR: Event already registed"
        QuizModel.callbacks[event] = func

    @staticmethod
    def emit(event: Callback, **data) -> None:
        assert event in QuizModel.callbacks, "ERROR: event not registred."
        func: Callable | None = QuizModel.callbacks[event]
        assert func, "ERROR: undefined callback"
        func(**data)

    @staticmethod
    def on_buzzer(player):
        if not QuizModel.is_waiting_buzzer:
            return

        QuizModel.is_waiting_buzzer = False
        QuizModel.current_player = player

        QuizModel.emit(
            Callback.BUZZER_ACTIVATED,
            player=player,
            name=QuizModel.player_1_name if player == 0 else QuizModel.player_2_name,
        )

    @staticmethod
    def answer(idx_choice: int) -> None:
        if not QuizModel.is_answering:
            return

        QuizModel.is_answering = False

        q = QuizModel.questions[QuizModel.q_index]
        correta = q["resposta"]
        acertou = idx_choice == correta

        resultado = {
            "acertou": acertou,
            "resposta_correta": correta,
            "resposta_escolhida": idx_choice,
            "jogador": QuizModel.current_player,
            "nome": (
                QuizModel.player_1_name
                if QuizModel.current_player == 0
                else QuizModel.player_2_name
            ),
            "nome_adversario": (
                QuizModel.player_2_name
                if QuizModel.current_player == 0
                else QuizModel.player_1_name
            ),
            "icon": None,
        }

        if acertou:
            QuizModel.points[QuizModel.current_player] += 1
            resultado["acao"] = "proximo"
            resultado["icon"] = QuizRes.correct_ans_icon
            resultado["msg"] = f"{resultado['nome']} acertou! +1 ponto!"

        elif QuizModel.first_try:
            QuizModel.first_try = False
            adversario = 1 - QuizModel.current_player
            resultado["icon"] = QuizRes.try_again_ans_icon
            resultado["acao"] = "segunda_chance"
            resultado["proximo_jogador"] = adversario
            resultado["msg"] = (
                f"{resultado['nome']} errou!\n"
                f"{resultado['nome_adversario']} tem a chance!"
            )

        else:
            resultado["acao"] = "proximo"
            resultado["icon"] = QuizRes.fail_ans
            resultado["msg"] = " Ninguém acertou! Próxima pergunta..."

        SerialManager.send("RESET")
        QuizModel.emit(Callback.ANSWER_PROCESSED, **resultado)

    @staticmethod
    def register_end_of_game() -> None:
        """Armazena o resultado na lista de histórico da sessão"""
        QuizModel.session_history.append(
            QuizGame(
                Player(QuizModel.player_1_name, QuizModel.points[PLAYER_1]),
                Player(QuizModel.player_2_name, QuizModel.points[PLAYER_2]),
                winner=(
                    PLAYER_1
                    if QuizModel.points[PLAYER_1] > QuizModel.points[PLAYER_2]
                    else PLAYER_2
                ),
            )
        )

    @staticmethod
    def restart() -> None:
        QuizModel.points = [0, 0]
        QuizModel.questions = random.sample(PERGUNTAS, TOTAL_PERGUNTAS)
        QuizModel.q_index = 0
        QuizModel.Question.load()

    @staticmethod
    def finish():
        SerialManager.disconnect()

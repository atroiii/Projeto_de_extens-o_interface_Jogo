"""Docs."""

from typing import Final, Optional, Callable
from enum import IntEnum, auto
from settings import Settings
from theme import Theme
from tkinter import messagebox
import tkinter as tk
import platform
from service.quizmodel import QuizModel, SerialManager
from callback import Callback
from quizfont import QuizFont, tkfont


class QuizUI(tk.Tk):
    """Docs."""

    class Create:
        @staticmethod
        def Card(master, **kw) -> tk.Frame:
            """Docs."""

            return tk.Frame(
                master,
                bg=Settings.COR_CARD,
                relief=Settings.Card.RELIEF,
                highlightthickness=1,
                highlightbackground="#34495e",
                padx=kw.pop("padx", 20),
                pady=kw.pop("pady", 20),
                **kw,
            )

        @staticmethod
        def Label(
            master,
            text: str,
            color: str = Settings.COR_TEXTO,
            font: Optional[tkfont.Font]=None,
            **kw
        ) -> tk.Label:
            """Docs."""
            if not font: font = QuizFont.median

            return tk.Label(
                master, text=text, bg=master["bg"], fg=color, font=font, **kw
            )

        @staticmethod
        def Button(
            master,
            text: str,
            cmd: str|Callable,
            bg_color: str = Settings.COR_BOTAO,
            fg_color: str = Settings.COR_TEXTO,
            font: Optional[tkfont.Font]=None,
            **kw
        ) -> tk.Button:
            """Docs."""
            if not font: font = QuizFont.choice

            return tk.Button(
                master,
                text=text,
                command=cmd,
                bg=bg_color,
                fg=fg_color,
                font=font,
                activebackground=Settings.COR_HOVER,
                activeforeground=Settings.COR_TITULO,
                relief=Settings.Button.RELIEF,
                cursor=Settings.Button.CURSOR,
                padx=Settings.Button.PADX,
                pady=Settings.Button.PADY,
                **kw,
            )

    class MenuEntry:
        player_1_name: tk.StringVar
        player_2_name: tk.StringVar
        serial_port: tk.StringVar

        @staticmethod
        def init() -> None:
            QuizUI.MenuEntry.player_1_name = tk.StringVar(value="Jogador 1")
            QuizUI.MenuEntry.player_2_name = tk.StringVar(value="Jogador 2")
            QuizUI.MenuEntry.serial_port = tk.StringVar(value="")
    
    class Screen:
        @staticmethod
        def menu(root) -> None:
            root.clear()

            top: Final[tk.Frame] = tk.Frame(root, bg=Settings.COR_BG)
            top.pack(fill="x", pady=30)

            QuizUI.Create.Label(
                top,
                Settings.Menu.TITLE,
                color=Settings.COR_OURO,
                font=QuizFont.title,
            ).pack()

            QuizUI.Create.Label(
                top,
                Settings.Menu.SUBTITLE,
                color=Settings.COR_TEXTO,
                font=QuizFont.small,
            ).pack(pady=10)

            # CONTEÚDO CENTRAL
            center = tk.Frame(root, bg=Settings.COR_BG)
            center.pack(expand=True)

            # Jogadores
            row_names = tk.Frame(center, bg=Settings.COR_BG)
            row_names.pack(pady=30)

            for i, (var, color) in enumerate([(QuizUI.MenuEntry.player_1_name, Settings.COR_P1), (QuizUI.MenuEntry.player_2_name, Settings.COR_P2)]):
                card = QuizUI.Create.Card(row_names, padx=40, pady=30)
                card.grid(row=0, column=i, padx=40)
            
                emoji = Settings.Menu.PLAYER_1_ICON if i == 0 else Settings.Menu.PLAYER_2_ICON
            
                QuizUI.Create.Label(
                    card, f"{emoji} Jogador {i + 1}", color=color, font=QuizFont.big
                ).pack()
            
                entry: tk.Entry = tk.Entry(
                    card,
                    textvariable=var,
                    font=QuizFont.median,
                    bg=Settings.COR_BOTAO,
                    fg=Settings.COR_TITULO,
                    insertbackground=Settings.COR_TITULO,
                    relief="flat",
                    justify="center",
                    width=20,
                )
                entry.pack(pady=15, ipady=10)

                def __focus_in(e, c=card, color_foco=color) -> None:
                    c.config(
                        highlightbackground=color_foco, highlightthickness=3
                    )

                def __focus_out(e, c=card):
                    c.config(
                        highlightbackground="#34495e", highlightthickness=1
                    )

                entry.bind("<FocusIn>", __focus_in)
                entry.bind("<FocusOut>", __focus_out)

            # Arduino
            arduino_card = QuizUI.Create.Card(center, padx=30, pady=20)
            arduino_card.pack(pady=20)
            
            QuizUI.Create.Label(
                arduino_card,
                Settings.Menu.ARDUINO_CONNECTION_MSG,
                color=Settings.COR_BUZZER,
                font=QuizFont.big,
            ).pack()
            
            port_row = tk.Frame(arduino_card, bg=Settings.COR_CARD)
            port_row.pack(pady=10)
            
            ports = SerialManager.ports_list()
            if ports:
                QuizUI.MenuEntry.serial_port.set(ports[0])
            
            QuizUI.Create.Label(port_row, "Porta COM:", color="#aaa", font=QuizFont.small).pack(
                side="left", padx=5
            )
            
            options = ports if ports else ["(nenhuma)"]
            
            root._menu_ports = tk.OptionMenu(port_row, QuizUI.MenuEntry.serial_port, *options)
            root._menu_ports.config(
                bg=Settings.COR_BOTAO,
                fg=Settings.COR_TEXTO,
                font=QuizFont.small,
                relief="flat",
                activebackground=Settings.COR_HOVER,
                highlightthickness=0,
            )
            root._menu_ports["menu"].config(bg=Settings.COR_BOTAO, fg=Settings.COR_TEXTO)
            root._menu_ports.pack(side="left", padx=10)
            
            QuizUI.Create.Button(
                port_row,
                "Atualizar",
                root.port_update,
                bg_color="#222",
                font=QuizFont.small,
            ).pack(side="left")
            
            # BOTÃO COMEÇAR
            QuizUI.Create.Button(
                root,
                "  COMEÇAR  ",
                root.game_init,
                bg_color=Settings.COR_OURO,
                fg_color="#1a1a2e",
                font=QuizFont.big,
            ).place(relx=0.50, rely=0.90, anchor="center")
            
            # BOTÃO TEMA
            QuizUI.Create.Button(root, "🎨", Theme.chance, font=tkfont.Font(size=40)).place(
                relx=0.98, rely=0.95, anchor="se", width=70, height=70
            )
            
            # BOTAO HISTORICO
            QuizUI.Create.Button(
                root,
                "📊 PLACAR DA SESSÃO",
                root.history_show,
                bg_color=Settings.COR_CARD,
                font=QuizFont.small,
            ).place(relx=0.02, rely=0.95, anchor="sw")

        @staticmethod
        def try_again(root) -> None:
            raise NotImplementedError("ERROR: try_again")


    def __init__(self) -> None:
        super().__init__()
        self.__keybinds()
        self.__window_config()
        QuizFont.init()
        QuizUI.MenuEntry.init()
        self.__regiter_callbacks()
        QuizUI.Screen.menu(self)

        self._menu_ports: tk.OptionMenu|None = None

    def __regiter_callbacks(self) -> None:
        """Docs."""

        QuizModel.register_callback(Callback.QUESTION_LOADED, self.__on_question_loaded)
        QuizModel.register_callback(
            Callback.BUZZER_ACTIVATED, self.__on_buzzer_activated
        )
        QuizModel.register_callback(
            Callback.ANSWER_PROCESSED, self.__on_answer_processed
        )
        QuizModel.register_callback(Callback.GAME_FINISHED, self.__on_game_fisished)

    def __keybinds(self) -> None:
        """Configura os atalhos de teclado."""

        self.bind(
            Settings.KEY_BUZZER_ACTIVATE_0, lambda e: QuizModel.buzzer_activate(0)
        )
        self.bind(
            Settings.KEY_BUZZER_ACTIVATE_1, lambda e: QuizModel.buzzer_activate(1)
        )

        self.bind(
            Settings.KEY_WINDOW_FULLSCREEN,
            lambda e: self.attributes(
                "-fullscreen", not self.attributes("-fullscreen")
            ),
        )

        self.bind(
            Settings.KEY_WINDOW_MINIMIZE,
            lambda e: self.attributes("-fullscreen", False),
        )

    def __window_config(self) -> None:
        """Configura a janela."""

        self.title(Settings.TITLE)

        # cross-platform
        if platform.system() == "Linux":
            self.attributes("-zoomed", True)
        elif platform.system() == "Windows":
            self.state("zoomed")
        else:
            messagebox.showwarning("Erro", "Seu sistema não é suportado.")

        self.resizable(True, True)
        self.configure(bg=Settings.COR_BG)
        Theme.apply(self)

    def __on_question_loaded(self, **data) -> None:
        """Docs."""

        raise NotImplementedError("ERROR: __on_question_loaded")

    def __on_buzzer_activated(self, **data) -> None:
        """Docs."""

        raise NotImplementedError("ERROR: __on_buzzer_activated")

    def __on_answer_processed(self, **data) -> None:
        """Docs."""

        raise NotImplementedError("ERROR: __on_answer_processed")

    def __on_game_fisished(self, **data) -> None:
        """Docs."""

        raise NotImplementedError("ERROR: __on_game_fisished")

    def clear(self) -> None:
        """Docs."""

        for w in self.winfo_children():
            w.destroy()

    def port_update(self) -> None:
        """Docs."""
        assert self._menu_ports, "ERROR: menu_ports not initialized"
        ports = SerialManager.ports_list()
        self._menu_ports["menu"].delete(0, "end")
        for p in ports:
            self._menu_ports["menu"].add_command(
                label=p, command=lambda v=p: QuizUI.MenuEntry.serial_port.set(v)
            )
        if ports:
            QuizUI.MenuEntry.serial_port.set(ports[0])

    def game_init(self) -> None:
        """Docs."""

        raise NotImplementedError("ERROR: ...")

    def history_show(self) -> None:
        """Docs."""

        raise NotImplementedError("ERROR: ...")

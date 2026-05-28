"""Docs."""

from typing import Final, Optional, Callable
from settings import Settings
from theme import Theme, FontTheme
from tkinter import messagebox
import tkinter as tk
import platform
from service.quizmodel import QuizModel, SerialManager
from callback import Callback
from quizfont import QuizFont, tkfont
from quizres import QuizRes


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
            color: str = Settings.COR_TITULO,
            font: Optional[tkfont.Font] = None,
            **kw,
        ) -> tk.Label:
            """Docs."""
            if not font:
                font = QuizFont.median

            return tk.Label(
                master, text=text, bg=master["bg"], fg=color, font=font, **kw
            )

        @staticmethod
        def Button(
            master,
            text: str,
            cmd: str | Callable,
            bg_color: str = Settings.COR_BOTAO,
            fg_color: str = Settings.COR_TITULO,
            font: Optional[tkfont.Font] = None,
            **kw,
        ) -> tk.Button:
            """Docs."""
            if not font:
                font = QuizFont.choice

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
        p1_avatar_idx: int = 0  # Começa no primeiro avatar
        p2_avatar_idx: int = 1  # Começa no segundo avatar

        @staticmethod
        def init() -> None:
            QuizUI.MenuEntry.player_1_name = tk.StringVar(value="A")
            QuizUI.MenuEntry.player_2_name = tk.StringVar(value="B")
            QuizUI.MenuEntry.serial_port = tk.StringVar(value="")
            QuizUI.MenuEntry.p1_avatar_idx = 0
            QuizUI.MenuEntry.p2_avatar_idx = 1

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

            center = tk.Frame(root, bg=Settings.COR_BG)
            center.pack(expand=True)

            row_names = tk.Frame(center, bg=Settings.COR_BG)
            row_names.pack(pady=30)

            lista_avatares = QuizRes.lista_todos_avatares

            # ==========================================
            # CARD DO JOGADOR 1 (ESQUERDA)
            # ==========================================
            card_p1 = QuizUI.Create.Card(row_names, padx=40, pady=30)
            card_p1.grid(row=0, column=0, padx=40)

            QuizUI.Create.Label(
                card_p1,
                "Jogador 1",
                color=Settings.COR_P1,
                font=QuizFont.big,
            ).pack()

            frame_p1 = tk.Frame(card_p1, bg=card_p1["bg"])
            frame_p1.pack(pady=10)

            lbl_avatar_p1 = tk.Label(
                frame_p1, 
                image=lista_avatares[QuizUI.MenuEntry.p1_avatar_idx], 
                bg=card_p1["bg"]
            )

            def mudar_avatar_p1(direcao):
                QuizUI.MenuEntry.p1_avatar_idx = (QuizUI.MenuEntry.p1_avatar_idx + direcao) % len(lista_avatares)
                lbl_avatar_p1.config(image=lista_avatares[QuizUI.MenuEntry.p1_avatar_idx])

            QuizUI.Create.Button(
                frame_p1, 
                "<", 
                lambda: mudar_avatar_p1(-1),
                bg_color=Settings.COR_BOTAO, 
                fg_color=Settings.COR_TITULO, 
                font=QuizFont.small
            ).pack(side="left", padx=10)

            lbl_avatar_p1.pack(side="left", padx=10)

            QuizUI.Create.Button(
                frame_p1, 
                ">", 
                lambda: mudar_avatar_p1(1),
                bg_color=Settings.COR_BOTAO, 
                fg_color=Settings.COR_TITULO, 
                font=QuizFont.small
            ).pack(side="left", padx=10)

            # Caixa de texto nativa do Tkinter para o Jogador 1
            entry_p1 = tk.Entry(
                card_p1,
                textvariable=QuizUI.MenuEntry.player_1_name,
                font=QuizFont.median,
                bg=Settings.COR_BOTAO,
                fg=Settings.COR_TITULO,
                insertbackground=Settings.COR_TITULO,
                relief="flat",
                justify="center",
                width=15
            )
            entry_p1.pack(pady=(10, 0), ipady=4)

            # ==========================================
            # CARD DO JOGADOR 2 (DIREITA)
            # ==========================================
            card_p2 = QuizUI.Create.Card(row_names, padx=40, pady=30)
            card_p2.grid(row=0, column=1, padx=40)

            QuizUI.Create.Label(
                card_p2,
                "Jogador 2",
                color=Settings.COR_P2,
                font=QuizFont.big,
            ).pack()

            frame_p2 = tk.Frame(card_p2, bg=card_p2["bg"])
            frame_p2.pack(pady=10)

            lbl_avatar_p2 = tk.Label(
                frame_p2, 
                image=lista_avatares[QuizUI.MenuEntry.p2_avatar_idx], 
                bg=card_p2["bg"]
            )

            def mudar_avatar_p2(direcao):
                QuizUI.MenuEntry.p2_avatar_idx = (QuizUI.MenuEntry.p2_avatar_idx + direcao) % len(lista_avatares)
                lbl_avatar_p2.config(image=lista_avatares[QuizUI.MenuEntry.p2_avatar_idx])

            QuizUI.Create.Button(
                frame_p2, 
                "<", 
                lambda: mudar_avatar_p2(-1),
                bg_color=Settings.COR_BOTAO, 
                fg_color=Settings.COR_TITULO, 
                font=QuizFont.small
            ).pack(side="left", padx=10)

            lbl_avatar_p2.pack(side="left", padx=10)

            QuizUI.Create.Button(
                frame_p2, 
                ">", 
                lambda: mudar_avatar_p2(1),
                bg_color=Settings.COR_BOTAO, 
                fg_color=Settings.COR_TITULO, 
                font=QuizFont.small
            ).pack(side="left", padx=10)

            # Caixa de texto nativa do Tkinter para o Jogador 2
            entry_p2 = tk.Entry(
                card_p2,
                textvariable=QuizUI.MenuEntry.player_2_name,
                font=QuizFont.median,
                bg=Settings.COR_BOTAO,
                fg=Settings.COR_TITULO,
                insertbackground=Settings.COR_TITULO,
                relief="flat",
                justify="center",
                width=15
            )
            entry_p2.pack(pady=(10, 0), ipady=4)

            # Conexão Arduino Card
            arduino_card = QuizUI.Create.Card(center, padx=30, pady=20)
            arduino_card.pack(pady=20)

            QuizUI.Create.Label(
                arduino_card,
                Settings.Menu.ARDUINO_CONNECTION_MSG,
                color=Settings.COR_BUZZER,
                font=QuizFont.big,
                image=QuizRes.ports_icon,
                compound="left",
            ).pack()

            port_row = tk.Frame(arduino_card, bg=Settings.COR_CARD)
            port_row.pack(pady=10)

            ports = SerialManager.ports_list()
            if ports:
                QuizUI.MenuEntry.serial_port.set(ports[0])

            QuizUI.Create.Label(
                port_row, "Porta COM:", color="#aaa", font=QuizFont.small
            ).pack(side="left", padx=5)

            options = ports if ports else ["(nenhuma)"]

            root.menu_ports = tk.OptionMenu(
                port_row, QuizUI.MenuEntry.serial_port, *options
            )
            root.menu_ports.config(
                bg=Settings.COR_BOTAO,
                fg=Settings.COR_TITULO,
                font=QuizFont.small,
                relief="flat",
                activebackground=Settings.COR_HOVER,
                highlightthickness=0,
            )
            root.menu_ports["menu"].config(bg=Settings.COR_BOTAO, fg=Settings.COR_TITULO)
            root.menu_ports.pack(side="left", padx=10)

            QuizUI.Create.Button(
                port_row,
                "",
                root.port_update,
                bg_color=Settings.COR_CARD,
                font=QuizFont.small,
                image=QuizRes.reload_ports_icon,
                borderwidth=0,
                highlightthickness=0,
            ).pack(side="left")

            QuizUI.Create.Button(
                root,
                Settings.Menu.BEGIN_BUTTON_MSG,
                root.game_init,
                bg_color=Settings.COR_OURO,
                fg_color="#1a1a2e",
                font=QuizFont.big,
            ).place(relx=0.50, rely=0.90, anchor="center")

            QuizUI.Create.Button(
                root,
                "",
                lambda: Theme.chance(root),
                font=tkfont.Font(size=40),
                image=QuizRes.theme_chance_icon,
            ).place(relx=0.98, rely=0.95, anchor="se", width=70, height=70)

            QuizUI.Create.Button(
                root,
                "Aa",
                lambda: FontTheme.chance(root),
                font=tkfont.Font(family="Arial", size=16, weight="bold"),
                bg_color=Settings.COR_CARD,
                fg_color=Settings.COR_TITULO,
            ).place(relx=0.92, rely=0.95, anchor="se", width=70, height=70)

            QuizUI.Create.Button(
                root,
                Settings.Menu.SCOREBOARD_BUTTON_MSG,
                root.history_show,
                bg_color=Settings.COR_CARD,
                font=QuizFont.small,
                image=QuizRes.history_icon,
                compound="left",
            ).place(relx=0.02, rely=0.95, anchor="sw")

        @staticmethod
        def try_again(root) -> None:
            """Exibe tela de segunda chance"""
            root.clear()
            QuizModel.is_answering = True

            progresso_container = tk.Frame(root, bg=Settings.COR_CARD, height=10)
            progresso_container.place(relx=0.5, rely=0.9, anchor="center", relwidth=0.8)

            total = 10
            largura = (QuizModel.q_index + 1) / total

            tk.Frame(progresso_container, bg=Settings.COR_OURO, height=10).place(
                relwidth=largura, relx=0
            )

            q = QuizModel.questions[QuizModel.q_index]
            cor = Settings.COR_P1 if QuizModel.current_player == 0 else Settings.COR_P2
            icon = (
                QuizRes.player_1_icon
                if QuizModel.current_player == 0
                else QuizRes.player_2_icon
            )

            nome = (
                QuizModel.player_1_name
                if QuizModel.current_player == 0
                else QuizModel.player_2_name
            )

            anuncio = tk.Frame(root, bg=Settings.COR_BG)
            anuncio.pack(fill="x", pady=(16, 4))
            QuizUI.Create.Label(
                anuncio,
                f"{nome} - segunda chance!",
                color=cor,
                font=QuizFont.big,
                image=icon,
                compound="left",
            ).pack()
            QuizUI.Create.Label(
                anuncio,
                "O adversário errou. Você sabe a resposta?",
                color=Settings.COR_BUZZER,
                font=QuizFont.small,
            ).pack(pady=(2, 0))

            tk.Frame(root, bg=cor, height=3).pack(fill="x", padx=20)

            c = QuizUI.Create.Card(root, padx=24, pady=14)
            c.pack(fill="x", padx=20, pady=8)
            QuizUI.Create.Label(
                c,
                q["pergunta"],
                color=Settings.COR_TITULO,
                font=QuizFont.big,
                wraplength=680,
                justify="center",
            ).pack()

            root.botoes_opcao = []
            for i, texto in enumerate(q["opcoes"]):
                letras = ["A", "B", "C", "D"]
                btn = QuizUI.Create.Button(
                    root,
                    f"  {letras[i]})  {texto}  ",
                    lambda idx=i: QuizModel.answer(idx),
                    bg_color=Settings.COR_BOTAO,
                    anchor="w",
                )
                btn.pack(fill="x", padx=20, pady=4, ipady=8)
                root.botoes_opcao.append(btn)

    def __init__(self) -> None:
        super().__init__()
        self.__keybinds()
        self.__window_config()
        QuizFont.init()
        QuizUI.MenuEntry.init()
        self.__regiter_callbacks()
        QuizRes.init()
        self.menu_ports: tk.OptionMenu | None = None
        QuizUI.Screen.menu(self)

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
            Settings.KEY_BUZZER_ACTIVATE_0, lambda e: QuizModel.on_buzzer(0)
        )
        self.bind(
            Settings.KEY_BUZZER_ACTIVATE_1, lambda e: QuizModel.on_buzzer(1)
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
        """Exibe tela de buzzer com as alternativas como botões"""
        self.clear()
        self.config(cursor="none")
        QuizModel.is_waiting_buzzer = True
        QuizModel.is_answering = False

        hdr = tk.Frame(self, bg=Settings.COR_BG)
        hdr.pack(fill="x", padx=20, pady=(18, 6))
        QuizUI.Create.Label(
            hdr,
            f"Pergunta {data['numero']} de {data['total']}",
            color="#aaa",
            font=QuizFont.small,
        ).pack(side="left")

        QuizUI.Create.Label(
            hdr,
            f"{data['nome_p1']}: {data['pontos_p1']}   "
            f"{data['nome_p2']}: {data['pontos_p2']}",
            color="#aaa",
            font=QuizFont.small,
        ).pack(side="right")

        progresso_container = tk.Frame(self, bg=Settings.COR_CARD, height=12)
        progresso_container.pack(side="bottom", fill="x", padx=60, pady=(0, 40))

        largura_proporcional = data["numero"] / data["total"]
        progresso_fill = tk.Frame(progresso_container, bg=Settings.COR_OURO, height=12)
        progresso_fill.place(relwidth=largura_proporcional, relx=0)

        tk.Frame(self, bg=Settings.COR_BUZZER, height=3).pack(fill="x", padx=20)

        c = QuizUI.Create.Card(self, padx=24, pady=18)
        c.pack(fill="x", padx=20, pady=12)
        QuizUI.Create.Label(
            c,
            data["pergunta"],
            color=Settings.COR_TITULO,
            font=QuizFont.big,
            wraplength=700,
            justify="center",
        ).pack()

        self.botoes_opcao = []
        for i, texto in enumerate(data["opcoes"]):
            letras = ["A", "B", "C", "D"]
            btn = QuizUI.Create.Button(
                self,
                f"  {letras[i]})  {texto}  ",
                lambda idx=i: None,
                bg_color=Settings.COR_BOTAO,
                anchor="w",
            )
            btn.config(state="disabled")
            btn.pack(fill="x", padx=20, pady=4, ipady=8)
            self.botoes_opcao.append(btn)

        wait = tk.Frame(self, bg=Settings.COR_BG)
        wait.pack(pady=16)
        QuizUI.Create.Label(
            wait,
            "QUEM SABE?",
            color=Settings.COR_BUZZER,
            font=QuizFont.buzzer,
            image=QuizRes.question_icon,
            compound="left",
        ).pack()
        QuizUI.Create.Label(
            wait,
            "Aperte o botão no Arduino para responder!",
            color="#aaa",
            font=QuizFont.small,
        ).pack(pady=(4, 0))

        self.update()
        self.config(cursor="")

    def __on_buzzer_activated(self, **data) -> None:
        """Exibe tela de resposta e ativa os botões"""
        self.clear()
        QuizModel.is_answering = True

        q = QuizModel.questions[QuizModel.q_index]
        cor = Settings.COR_P1 if data["player"] == 0 else Settings.COR_P2
        icon = QuizRes.player_1_icon if data["player"] == 0 else QuizRes.player_2_icon

        anuncio = tk.Frame(self, bg=Settings.COR_BG)
        anuncio.pack(fill="x", pady=(16, 4))
        QuizUI.Create.Label(
            anuncio,
            f"  {data['name']} respondeu primeiro!",
            color=cor,
            font=QuizFont.big,
            image=icon,
            compound="left",
        ).pack()
        QuizUI.Create.Label(
            anuncio, "Escolha a resposta correta:", color="#aaa", font=QuizFont.small
        ).pack(pady=(2, 0))

        tk.Frame(self, bg=cor, height=3).pack(fill="x", padx=20)

        c = QuizUI.Create.Card(self, padx=24, pady=14)
        c.pack(fill="x", padx=20, pady=8)
        QuizUI.Create.Label(
            c,
            q["pergunta"],
            color=Settings.COR_TITULO,
            font=QuizFont.big,
            wraplength=680,
            justify="center",
        ).pack()

        self.botoes_opcao = []
        for i, texto in enumerate(q["opcoes"]):
            letras = ["A", "B", "C", "D"]
            btn = QuizUI.Create.Button(
                self,
                f"  {letras[i]})  {texto}  ",
                lambda idx=i: QuizModel.answer(idx),
                bg_color=Settings.COR_BOTAO,
                anchor="w",
            )
            btn.pack(fill="x", padx=20, pady=4, ipady=8)
            self.botoes_opcao.append(btn)

    def __on_answer_processed(self, **data) -> None:
        """Processa resultado da resposta"""
        for btn in self.botoes_opcao:
            btn.config(state="disabled")

        if not data["acertou"]:
            self.botoes_opcao[data["resposta_escolhida"]].config(
                bg=Settings.COR_ERRADO, fg="#1a1a2e"
            )

        cor_msg = Settings.COR_CERTO if data["acertou"] else Settings.COR_ERRADO
        tk.Label(
            self,
            text=data["msg"],
            bg=Settings.COR_BG,
            fg=cor_msg,
            font=QuizFont.big,
            wraplength=680,
            justify="center",
            image=data["icon"],
            compound="left",
        ).pack(pady=10)

        if data["acao"] == "segunda_chance":
            QuizModel.current_player = data["proximo_jogador"]
            self.after(2200, lambda: QuizUI.Screen.try_again(self))
        else:
            self.after(1800 if data["acertou"] else 2000, QuizModel.Question.next)

    def __on_game_fisished(self, **data) -> None:
        """Exibe tela de resultado"""
        self.clear()

        p1, p2 = data["pontos_p1"], data["pontos_p2"]

        if p1 > p2:
            vencedor, cor_v = data["nome_p1"], Settings.COR_P1
        elif p2 > p1:
            vencedor, cor_v = data["nome_p2"], Settings.COR_P2
        else:
            vencedor, cor_v = "Empate!", Settings.COR_OURO

        tk.Frame(self, bg=Settings.COR_BG).pack(expand=True)
        QuizUI.Create.Label(
            self,
            " RESULTADO FINAL",
            color=Settings.COR_OURO,
            font=QuizFont.title,
            image=QuizRes.winner_icon,
            compound="left",
        ).pack()

        c = QuizUI.Create.Card(self, padx=40, pady=24)
        c.pack(padx=60, pady=20)
        row = tk.Frame(c, bg=Settings.COR_CARD)
        row.pack()
        for nome, pts, cor, em in [
            (data["nome_p1"], p1, Settings.COR_P1, QuizRes.player_1_icon),
            (data["nome_p2"], p2, Settings.COR_P2, QuizRes.player_2_icon),
        ]:
            col = tk.Frame(row, bg=Settings.COR_CARD, padx=30)
            col.pack(side="left")
            QuizUI.Create.Label(
                col, f"{nome}", color=cor, font=QuizFont.big, image=em, compound="left"
            ).pack()
            QuizUI.Create.Label(
                col,
                f"{pts}",
                color=Settings.COR_TITULO,
                font=tkfont.Font(family="Arial", size=48, weight="bold"),
            ).pack()
            QuizUI.Create.Label(col, "pontos", color="#888", font=QuizFont.small).pack()

        QuizUI.Create.Label(self, vencedor, color=cor_v, font=QuizFont.title).pack(
            pady=(0, 4)
        )

        btns = tk.Frame(self, bg=Settings.COR_BG)
        btns.pack(pady=16)
        QuizUI.Create.Button(
            btns,
            "  JOGAR NOVAMENTE  ",
            QuizModel.restart,
            bg_color=Settings.COR_OURO,
            fg_color="#1a1a2e",
            font=QuizFont.big,
        ).pack(side="left", padx=8, ipadx=8, ipady=4)
        QuizUI.Create.Button(
            btns, "  MENU INICIAL  ", self.back_to_menu, bg_color=Settings.COR_BOTAO
        ).pack(side="left", padx=8, ipadx=8, ipady=4)
        tk.Frame(self, bg=Settings.COR_BG).pack(expand=True)

    def update_menu(self) -> None:
        QuizUI.Screen.menu(self)

    def clear(self) -> None:
        """Docs."""
        for w in self.winfo_children():
            w.destroy()

    def port_update(self) -> None:
        """Docs."""
        assert self.menu_ports is not None, "ERROR: Menu port não inicializado."

        ports = SerialManager.ports_list()
        self.menu_ports["menu"].delete(0, "end")
        for p in ports:
            self.menu_ports["menu"].add_command(
                label=p, command=lambda v=p: QuizUI.MenuEntry.serial_port.set(v)
            )
        if ports:
            QuizUI.MenuEntry.serial_port.set(ports[0])

    def game_init(self) -> None:
        """Docs."""
        port = QuizUI.MenuEntry.serial_port.get()

        if port == "(nenhuma)":
            messagebox.showwarning("Warning", "Nenhuma porta selecionada.")
            port = ""

        # LISTA DE AVATARES IDENTICA AO DO PASSO 2
        lista_avatares = [
            QuizRes.player_1_icon, 
            QuizRes.player_2_icon,
            QuizRes.question_icon,
            QuizRes.winner_icon
        ]

        # RECONFIGURA OS ICONES OFICIAIS COM OS QUE OS JOGADORES ESCOLHERAM NAS SETAS!
        QuizRes.player_1_icon = lista_avatares[QuizUI.MenuEntry.p1_avatar_idx]
        QuizRes.player_2_icon = lista_avatares[QuizUI.MenuEntry.p2_avatar_idx]

        QuizModel.init(
            QuizUI.MenuEntry.player_1_name.get(),
            QuizUI.MenuEntry.player_2_name.get(),
            port,
        )

    def history_show(self) -> None:
        """Docs."""
        window = tk.Toplevel(self)
        window.title(Settings.History.WINDOW_TITLE)
        window.geometry(Settings.History.WINDOW_RES)
        window.configure(bg=Settings.COR_BG)

        QuizUI.Create.Label(
            window,
            Settings.History.TITLE,
            color=Settings.COR_OURO,
            font=QuizFont.big,
            image=QuizRes.history_icon,
            compound="left",
        ).pack(pady=20)

        if len(QuizModel.session_history) <= 0:
            QuizUI.Create.Label(
                window, Settings.History.NOGAMES_MSG, color="#888"
            ).pack(pady=50)
            return

        container = tk.Frame(window, bg=Settings.COR_BG)
        container.pack(fill="both", expand=True, padx=20)

        for i, game in enumerate(reversed(QuizModel.session_history)):
            card = QuizUI.Create.Card(container)
            card.pack(fill="x", pady=5, ipady=5)

            texto = (
                f"JOGO {len(QuizModel.session_history) - i}\n"
                f"{game.player_1.name} [{game.player_1.points}] x [{game.player_2.points}] {game.player_2.name}"
            )

            QuizUI.Create.Label(card, texto, font=QuizFont.small).pack()
            QuizUI.Create.Label(
                card,
                f"Vencedor: {game.player_1.name if (game.winner == 0) else game.player_2.name}",
                color=Settings.COR_OURO,
                font=QuizFont.small,
            ).pack()

    def back_to_menu(self) -> None:
        QuizModel.finish()
        self.Screen.menu(self)

    def destroy(self):
        QuizModel.finish()
        super().destroy()

import tkinter as tk
from tkinter import font as tkfont
from Service.quiz_logica import QuizModel

TEMAS = [
    {
        "nome": "Jogo",
        "BG": "#0d1b2a",
        "CARD": "#1b263b",
        "BOTAO": "#415a77",
        "HOVER": "#778da9",
        "TEXTO": "#e0e1dd",
        "TITULO": "#ffffff",
        "OURO": "#ffd60a",
        "BUZZER": "#ff6b00",
        "P1": "#4cc9f0",
        "P2": "#f72585",
    },
    {
        "nome": "Padrao",
        "BG": "#121212",
        "CARD": "#1e1e1e",
        "BOTAO": "#2c2c2c",
        "HOVER": "#3a3a3a",
        "TEXTO": "#e0e0e0",
        "TITULO": "#ffffff",
        "OURO": "#f9c74f",
        "BUZZER": "#f8961e",
        "P1": "#90caf9",
        "P2": "#f48fb1",
    },
    {
        "nome": "Neon",
        "BG": "#0f0f1a",
        "CARD": "#1a1a2e",
        "BOTAO": "#16213e",
        "HOVER": "#0f3460",
        "TEXTO": "#eaeaea",
        "TITULO": "#ffffff",
        "OURO": "#00f5d4",
        "BUZZER": "#ff006e",
        "P1": "#3a86ff",
        "P2": "#ff006e",
    }
]

#CORES
COR_BG = "#0f0f1a"
COR_CARD = "#1a1a2e"
COR_BOTAO = "#16213e"
COR_HOVER = "#0f3460"

COR_TEXTO = "#eaeaea"
COR_TITULO = "#ffffff"

COR_OURO = "#00f5d4"
COR_BUZZER = "#ff006e"

COR_P1 = "#3a86ff"
COR_P2 = "#ff006e"

COR_CERTO = "#06d6a0"
COR_ERRADO = "#ef476f"


class QuizUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz – Dois Jogadores (Arduino Buzzer)")
        self.geometry("1920x1080")
        self.resizable(False, False)
        self.configure(bg=COR_BG)

        self.tema_index = 0
        self._aplicar_tema()


        # Configurar fonts
        fonte_base = "Comic Sans Ms"
        self.fonte_titulo = tkfont.Font(family="Impact", size=42, weight="bold")
        self.fonte_grande = tkfont.Font(family=fonte_base, size=16, weight="bold")
        self.fonte_media = tkfont.Font(family=fonte_base, size=13)
        self.fonte_pequena = tkfont.Font(family=fonte_base, size=11)
        self.fonte_opcao = tkfont.Font(family=fonte_base, size=13, weight="bold")
        self.fonte_buzzer = tkfont.Font(family=fonte_base, size=22, weight="bold")

        # StringVars
        self.nome_p1 = tk.StringVar(value="Jogador 1")
        self.nome_p2 = tk.StringVar(value="Jogador 2")
        self.porta_serial = tk.StringVar(value="")

        # Model
        self.model = QuizModel()
        self._registrar_callbacks()

        self._tela_inicial()

    def _registrar_callbacks(self):
        self.model.registrar_callback('pergunta_carregada', self._on_pergunta_carregada)
        self.model.registrar_callback('buzzer_ativado', self._on_buzzer_ativado)
        self.model.registrar_callback('resposta_processada', self._on_resposta_processada)
        self.model.registrar_callback('jogo_finalizado', self._on_jogo_finalizado)

    def _limpar(self):
        for w in self.winfo_children():
            w.destroy()

    def _card(self, master, **kw):
        return tk.Frame(master, bg=COR_CARD, relief="flat", **kw)

    def _label(self, master, texto, cor=COR_TEXTO, fonte=None, **kw):
        if fonte is None:
            fonte = self.fonte_media
        return tk.Label(master, text=texto, bg=master["bg"],
                        fg=cor, font=fonte, **kw)

    def _botao(self, master, texto, cmd, cor_bg=COR_BOTAO,
               cor_fg=COR_TEXTO, fonte=None, **kw):
        if fonte is None:
            fonte = self.fonte_opcao
        return tk.Button(master, text=texto, command=cmd,
                         bg=cor_bg, fg=cor_fg, font=fonte,
                         activebackground=COR_HOVER,
                         activeforeground=COR_TITULO,
                         relief="flat", cursor="hand2",
                         padx=10, pady=6, **kw)
    
    def _atualizar_portas(self):  # 👈 TEM QUE EXISTIR
        portas = self.model.serial_manager.listar_portas()
        self._menu_portas["menu"].delete(0, "end")
        for p in portas:
            self._menu_portas["menu"].add_command(
                label=p, command=lambda v=p: self.porta_serial.set(v))
        if portas:
            self.porta_serial.set(portas[0])

    def _iniciar_jogo(self):
        porta = self.porta_serial.get()

        if porta == "(nenhuma)":
            porta = None

        self.model.inicializar(
            self.nome_p1.get(),
            self.nome_p2.get(),
            porta
        )

    def _aplicar_tema(self):
        tema = TEMAS[self.tema_index]

        global COR_BG, COR_CARD, COR_BOTAO, COR_HOVER
        global COR_TEXTO, COR_TITULO, COR_OURO, COR_BUZZER
        global COR_P1, COR_P2

        COR_BG = tema["BG"]
        COR_CARD = tema["CARD"]
        COR_BOTAO = tema["BOTAO"]
        COR_HOVER = tema["HOVER"]
        COR_TEXTO = tema["TEXTO"]
        COR_TITULO = tema["TITULO"]
        COR_OURO = tema["OURO"]
        COR_BUZZER = tema["BUZZER"]
        COR_P1 = tema["P1"]
        COR_P2 = tema["P2"]

        self.configure(bg=COR_BG)


    def _trocar_tema(self):
        self.tema_index = (self.tema_index + 1) % len(TEMAS)
        self._aplicar_tema()
        self._tela_inicial()  # redesenha a tela

        # ── Tela Inicial ──────────────────────────────────────────
    
    def _tela_inicial(self):
        self._limpar()

        # ── TOPO (HEADER) ─────────────────────────
        topo = tk.Frame(self, bg=COR_BG)
        topo.pack(fill="x", pady=40)

        self._label(topo, "🎯 QUIZ DOIS JOGADORES",
                    cor=COR_OURO, fonte=self.fonte_titulo).pack()

        self._label(topo, "10 perguntas · Quem errar passa a vez!",
                    cor=COR_TEXTO, fonte=self.fonte_pequena).pack(pady=20)

        # ── MEIO (CONTEÚDO CENTRAL) ──────────────
        meio = tk.Frame(self, bg=COR_BG)
        meio.pack(expand=True)

        # Jogadores
        row_nomes = tk.Frame(meio, bg=COR_BG)
        row_nomes.pack(pady=40)

        for i, (var, cor) in enumerate([(self.nome_p1, COR_P1),
                                        (self.nome_p2, COR_P2)]):

            c = self._card(row_nomes, padx=40, pady=30)
            c.grid(row=0, column=i, padx=40)

            emoji = "🔵" if i == 0 else "🔴"

            self._label(c, f"{emoji} Jogador {i + 1}",
                        cor=cor, fonte=self.fonte_grande).pack()

            tk.Entry(c, textvariable=var,
                    font=self.fonte_media,
                    bg="#0f3460", fg=COR_TITULO,
                    insertbackground=COR_TITULO,
                    relief="flat", justify="center",
                    width=40).pack(pady=30, ipady=25)

        # Arduino (mais centralizado tipo card)
        arduino_card = self._card(meio, padx=40, pady=30)
        arduino_card.pack(pady=30)

        self._label(arduino_card, "⚡ Conexão Arduino",
                    cor=COR_BUZZER, fonte=self.fonte_grande).pack()

        porta_row = tk.Frame(arduino_card, bg=COR_CARD)
        porta_row.pack(pady=20)

        portas = self.model.serial_manager.listar_portas()
        if portas:
            self.porta_serial.set(portas[0])

        self._label(porta_row, "Porta COM:",
                    cor="#aaa", fonte=self.fonte_pequena).pack(side="left", padx=5)

        opcoes = portas if portas else ["(nenhuma)"]

        self._menu_portas = tk.OptionMenu(porta_row, self.porta_serial, *opcoes)
        self._menu_portas.config(bg=COR_BOTAO, fg=COR_TEXTO,
                                font=self.fonte_pequena, relief="flat",
                                activebackground=COR_HOVER, highlightthickness=0)
        self._menu_portas["menu"].config(bg=COR_BOTAO, fg=COR_TEXTO)
        self._menu_portas.pack(side="left", padx=10)

        self._botao(porta_row, "Atualizar",
                    self._atualizar_portas,
                    cor_bg="#222",
                    fonte=self.fonte_pequena).pack(side="left")

        # ── RODAPÉ (BOTÃO) ───────────────────────
        baixo = tk.Frame(self, bg=COR_BG)
        baixo.pack(pady=40)

        self._botao(baixo, "  COMEÇAR  ",
                    self._iniciar_jogo,
                    cor_bg=COR_OURO,
                    cor_fg="#1a1a2e",
                    fonte=self.fonte_grande).pack(ipadx=40, ipady=30)
        
        self._botao(
                    baixo,
                    "🎨 Tema",
                    self._trocar_tema,
                    cor_bg=COR_BOTAO,
                    fonte=self.fonte_pequena
                ).pack(pady=10)

    # ── Callbacks do Model ────────────────────────────────────
    def _on_pergunta_carregada(self, **dados):
        """Exibe tela de buzzer"""
        self._limpar()
        self.model.aguardando_buzzer = True
        self.model.respondendo = False

        hdr = tk.Frame(self, bg=COR_BG)
        hdr.pack(fill="x", padx=20, pady=(18, 6))
        self._label(hdr, f"Pergunta {dados['numero']} de {dados['total']}",
                    cor="#aaa", fonte=self.fonte_pequena).pack(side="left")
        self._label(hdr,
                    f"🔵 {dados['nome_p1']}: {dados['pontos_p1']}   "
                    f"🔴 {dados['nome_p2']}: {dados['pontos_p2']}",
                    cor="#aaa", fonte=self.fonte_pequena).pack(side="right")

        tk.Frame(self, bg=COR_BUZZER, height=3).pack(fill="x", padx=20)

        c = self._card(self, padx=24, pady=18)
        c.pack(fill="x", padx=20, pady=12)
        self._label(c, dados['pergunta'], cor=COR_TITULO, fonte=self.fonte_grande,
                    wraplength=700, justify="center").pack()

        wait = tk.Frame(self, bg=COR_BG)
        wait.pack(pady=16)
        self._label(wait, "⚡  QUEM SABE?", cor=COR_BUZZER,
                    fonte=self.fonte_buzzer).pack()
        self._label(wait, "Aperte o botão no Arduino para responder!",
                    cor="#aaa", fonte=self.fonte_pequena).pack(pady=(4, 0))

    def _on_buzzer_ativado(self, **dados):
        """Exibe tela de resposta"""
        self._limpar()
        self.model.respondendo = True

        q = self.model.perguntas[self.model.q_index]
        cor = COR_P1 if dados['jogador'] == 0 else COR_P2
        emoji = "🔵" if dados['jogador'] == 0 else "🔴"

        anuncio = tk.Frame(self, bg=COR_BG)
        anuncio.pack(fill="x", pady=(16, 4))
        self._label(anuncio,
                    f"{emoji}  {dados['nome']} respondeu primeiro!",
                    cor=cor, fonte=self.fonte_grande).pack()
        self._label(anuncio, "Escolha a resposta correta:",
                    cor="#aaa", fonte=self.fonte_pequena).pack(pady=(2, 0))

        tk.Frame(self, bg=cor, height=3).pack(fill="x", padx=20)

        c = self._card(self, padx=24, pady=14)
        c.pack(fill="x", padx=20, pady=8)
        self._label(c, q["pergunta"], cor=COR_TITULO, fonte=self.fonte_grande,
                    wraplength=680, justify="center").pack()

        self.botoes_opcao = []
        for i, texto in enumerate(q["opcoes"]):
            letras = ["A", "B", "C", "D"]
            btn = self._botao(self, f"  {letras[i]})  {texto}  ",
                              lambda idx=i: self.model.responder(idx),
                              cor_bg=COR_BOTAO, anchor="w")
            btn.pack(fill="x", padx=20, pady=4, ipady=8)
            self.botoes_opcao.append(btn)

    def _on_resposta_processada(self, **dados):
        """Processa resultado da resposta"""
        for btn in self.botoes_opcao:
            btn.config(state="disabled")


        if not dados['acertou']:
            self.botoes_opcao[dados['resposta_escolhida']].config(bg=COR_ERRADO, fg="#1a1a2e")

        cor_msg = COR_CERTO if dados['acertou'] else COR_ERRADO
        tk.Label(self, text=dados['msg'], bg=COR_BG, fg=cor_msg,
                 font=self.fonte_grande,
                 wraplength=680, justify="center").pack(pady=10)

        if dados['acao'] == 'segunda_chance':
            self.model.vez_atual = dados['proximo_jogador']
            self.after(2200, self._exibir_segunda_chance)
        else:
            self.after(1800 if dados['acertou'] else 2000, self.model.proxima_pergunta)

    def _exibir_segunda_chance(self):
        """Exibe tela de segunda chance"""
        self._limpar()
        self.model.respondendo = True

        q = self.model.perguntas[self.model.q_index]
        cor = COR_P1 if self.model.vez_atual == 0 else COR_P2
        emoji = "🔵" if self.model.vez_atual == 0 else "🔴"
        nome = self.model.nome_p1 if self.model.vez_atual == 0 else self.model.nome_p2

        anuncio = tk.Frame(self, bg=COR_BG)
        anuncio.pack(fill="x", pady=(16, 4))
        self._label(anuncio,
                    f"{emoji}  {nome} — segunda chance!",
                    cor=cor, fonte=self.fonte_grande).pack()
        self._label(anuncio, "O adversário errou. Você sabe a resposta?",
                    cor=COR_BUZZER, fonte=self.fonte_pequena).pack(pady=(2, 0))

        tk.Frame(self, bg=cor, height=3).pack(fill="x", padx=20)

        c = self._card(self, padx=24, pady=14)
        c.pack(fill="x", padx=20, pady=8)
        self._label(c, q["pergunta"], cor=COR_TITULO, fonte=self.fonte_grande,
                    wraplength=680, justify="center").pack()

        self.botoes_opcao = []
        for i, texto in enumerate(q["opcoes"]):
            letras = ["A", "B", "C", "D"]
            btn = self._botao(self, f"  {letras[i]})  {texto}  ",
                              lambda idx=i: self.model.responder(idx),
                              cor_bg=COR_BOTAO, anchor="w")
            btn.pack(fill="x", padx=20, pady=4, ipady=8)
            self.botoes_opcao.append(btn)

    def _on_jogo_finalizado(self, **dados):
        """Exibe tela de resultado"""
        self._limpar()

        p1, p2 = dados['pontos_p1'], dados['pontos_p2']

        if p1 > p2:
            vencedor, cor_v = dados['nome_p1'], COR_P1
        elif p2 > p1:
            vencedor, cor_v = dados['nome_p2'], COR_P2
        else:
            vencedor, cor_v = "Empate!", COR_OURO

        tk.Frame(self, bg=COR_BG).pack(expand=True)
        self._label(self, "🏆  RESULTADO FINAL", cor=COR_OURO,
                    fonte=self.fonte_titulo).pack()

        c = self._card(self, padx=40, pady=24)
        c.pack(padx=60, pady=20)
        row = tk.Frame(c, bg=COR_CARD)
        row.pack()
        for nome, pts, cor, em in [(dados['nome_p1'], p1, COR_P1, "🔵"),
                                   (dados['nome_p2'], p2, COR_P2, "🔴")]:
            col = tk.Frame(row, bg=COR_CARD, padx=30)
            col.pack(side="left")
            self._label(col, f"{em} {nome}", cor=cor,
                        fonte=self.fonte_grande).pack()
            self._label(col, f"{pts}", cor=COR_TITULO,
                        fonte=tkfont.Font(family="Arial", size=48,
                                          weight="bold")).pack()
            self._label(col, "pontos", cor="#888",
                        fonte=self.fonte_pequena).pack()

        self._label(self, vencedor, cor=cor_v,
                    fonte=self.fonte_titulo).pack(pady=(0, 4))

        btns = tk.Frame(self, bg=COR_BG)
        btns.pack(pady=16)
        self._botao(btns, "  JOGAR NOVAMENTE  ", self.model.reiniciar,
                    cor_bg=COR_OURO, cor_fg="#1a1a2e",
                    fonte=self.fonte_grande).pack(side="left", padx=8,
                                                  ipadx=8, ipady=4)
        self._botao(btns, "  MENU INICIAL  ", self._voltar_menu,
                    cor_bg=COR_BOTAO).pack(side="left", padx=8,
                                           ipadx=8, ipady=4)
        tk.Frame(self, bg=COR_BG).pack(expand=True)

    def _voltar_menu(self):
        self.model.encerrar()
        self._tela_inicial()

    def destroy(self):
        self.model.encerrar()
        super().destroy()


if __name__ == "__main__":
    app = QuizUI()
    app.mainloop()

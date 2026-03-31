
import tkinter as tk
from tkinter import font as tkfont
import random
import threading
import serial
import serial.tools.list_ports

BAUD_RATE = 9600

PERGUNTAS = [
    {"pergunta": "Qual é a capital do Brasil?",
     "opcoes": ["São Paulo", "Brasília", "Rio de Janeiro", "Salvador"],
     "resposta": 1},
    {"pergunta": "Quantos estados tem o Brasil?",
     "opcoes": ["24", "25", "26", "27"],
     "resposta": 2},
    {"pergunta": "Quem escreveu 'Dom Casmurro'?",
     "opcoes": ["José de Alencar", "Machado de Assis", "Guimarães Rosa", "Clarice Lispector"],
     "resposta": 1},
    {"pergunta": "Qual é o maior planeta do Sistema Solar?",
     "opcoes": ["Saturno", "Netuno", "Júpiter", "Urano"],
     "resposta": 2},
    {"pergunta": "Em que ano o Brasil foi descoberto?",
     "opcoes": ["1492", "1498", "1500", "1502"],
     "resposta": 2},
    {"pergunta": "Qual é o elemento químico representado por 'O'?",
     "opcoes": ["Ouro", "Osmio", "Oxigênio", "Ósmio"],
     "resposta": 2},
    {"pergunta": "Quantos jogadores tem um time de futebol em campo?",
     "opcoes": ["9", "10", "11", "12"],
     "resposta": 2},
    {"pergunta": "Qual é a montanha mais alta do mundo?",
     "opcoes": ["K2", "Monte Everest", "Aconcágua", "Mont Blanc"],
     "resposta": 1},
    {"pergunta": "Qual país tem a maior população do mundo?",
     "opcoes": ["Índia", "EUA", "China", "Rússia"],
     "resposta": 0},
    {"pergunta": "Quantos lados tem um hexágono?",
     "opcoes": ["5", "6", "7", "8"],
     "resposta": 1},
    {"pergunta": "Qual é o idioma oficial do Brasil?",
     "opcoes": ["Espanhol", "Inglês", "Português", "Guarani"],
     "resposta": 2},
    {"pergunta": "Qual é o osso mais longo do corpo humano?",
     "opcoes": ["Úmero", "Rádio", "Fêmur", "Tíbia"],
     "resposta": 2},
    {"pergunta": "Quem pintou a Mona Lisa?",
     "opcoes": ["Michelangelo", "Raphael", "Leonardo da Vinci", "Donatello"],
     "resposta": 2},
    {"pergunta": "Qual é a fórmula química da água?",
     "opcoes": ["CO2", "H2O", "O2", "NaCl"],
     "resposta": 1},
    {"pergunta": "Quantas horas tem um dia?",
     "opcoes": ["12", "48", "24", "36"],
     "resposta": 2},
]

COR_BG     = "#1a1a2e"
COR_CARD   = "#16213e"
COR_P1     = "#4fc3f7"
COR_P2     = "#ef9a9a"
COR_CERTO  = "#81c784"
COR_ERRADO = "#e57373"
COR_BOTAO  = "#0f3460"
COR_HOVER  = "#533483"
COR_TEXTO  = "#e0e0e0"
COR_TITULO = "#ffffff"
COR_OURO   = "#ffd700"
COR_BUZZER = "#ff9800"

TOTAL_PERGUNTAS = 10


class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz – Dois Jogadores (Arduino Buzzer)")
        self.geometry("1920x1080")
        self.resizable(False, False)
        self.configure(bg=COR_BG)

        self.fonte_titulo  = tkfont.Font(family="Arial", size=28, weight="bold")
        self.fonte_grande  = tkfont.Font(family="Arial", size=16, weight="bold")
        self.fonte_media   = tkfont.Font(family="Arial", size=13)
        self.fonte_pequena = tkfont.Font(family="Arial", size=11)
        self.fonte_opcao   = tkfont.Font(family="Arial", size=13, weight="bold")
        self.fonte_buzzer  = tkfont.Font(family="Arial", size=22, weight="bold")

        self.nome_p1      = tk.StringVar(value="Jogador 1")
        self.nome_p2      = tk.StringVar(value="Jogador 2")
        self.porta_serial = tk.StringVar(value="")
        self.pontos       = [0, 0]

        self.serial_conn     = None
        self._serial_running = False

        self.perguntas          = []
        self.q_index            = 0
        self.vez_atual          = 0
        self.primeira_tentativa = True
        self.aguardando_buzzer  = False
        self.respondendo        = False

        self._tela_inicial()

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

    # ── Serial ────────────────────────────────────────────────────────────────
    def _listar_portas(self):
        return [p.device for p in serial.tools.list_ports.comports()]

    def _conectar_serial(self, porta):
        try:
            self.serial_conn = serial.Serial(porta, BAUD_RATE, timeout=0.1)
            self._serial_running = True
            threading.Thread(target=self._ler_serial, daemon=True).start()
            return True
        except Exception as e:
            print(f"Erro serial: {e}")
            return False

    def _ler_serial(self):
        while self._serial_running and self.serial_conn:
            try:
                if self.serial_conn.in_waiting:
                    linha = self.serial_conn.readline().decode("utf-8").strip()
                    if linha in ("1", "2") and self.aguardando_buzzer:
                        jogador = int(linha) - 1
                        self.after(0, lambda j=jogador: self._buzzer_ativado(j))
            except Exception:
                break

    def _enviar_serial(self, cmd):
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write((cmd + "\n").encode())
            except Exception:
                pass

    # ── Tela inicial ──────────────────────────────────────────────────────────
    def _tela_inicial(self):
        self._limpar()

        hdr = tk.Frame(self, bg=COR_BG)
        hdr.pack(fill="x", pady=(24, 8))
        self._label(hdr, "🎯 QUIZ DOIS JOGADORES", cor=COR_OURO,
                    fonte=self.fonte_titulo).pack()
        self._label(hdr, f"{TOTAL_PERGUNTAS} perguntas · Quem errar passa a vez!",
                    cor=COR_TEXTO, fonte=self.fonte_pequena).pack(pady=(4, 0))

        row_nomes = tk.Frame(self, bg=COR_BG)
        row_nomes.pack(pady=(16, 8))
        for i, (var, cor) in enumerate([(self.nome_p1, COR_P1),
                                         (self.nome_p2, COR_P2)]):
            c = self._card(row_nomes, padx=20, pady=14)
            c.grid(row=0, column=i, padx=14)
            emoji = "🔵" if i == 0 else "🔴"
            self._label(c, f"{emoji}  Jogador {i+1}", cor=cor,
                        fonte=self.fonte_grande).pack()
            entry = tk.Entry(c, textvariable=var, font=self.fonte_media,
                             bg="#0f3460", fg=COR_TITULO,
                             insertbackground=COR_TITULO,
                             relief="flat", justify="center", width=18)
            entry.pack(pady=(10, 0), ipady=6)

        arduino_card = self._card(self, padx=24, pady=14)
        arduino_card.pack(padx=60, pady=(4, 0), fill="x")
        self._label(arduino_card, "⚡  Conexão Arduino",
                    cor=COR_BUZZER, fonte=self.fonte_grande).pack()

        porta_row = tk.Frame(arduino_card, bg=COR_CARD)
        porta_row.pack(pady=(10, 0))
        portas = self._listar_portas()
        if portas:
            self.porta_serial.set(portas[0])
        self._label(porta_row, "Porta COM:", cor="#aaa",
                    fonte=self.fonte_pequena).pack(side="left", padx=(0, 8))
        opcoes = portas if portas else ["(nenhuma)"]
        self._menu_portas = tk.OptionMenu(porta_row, self.porta_serial, *opcoes)
        self._menu_portas.config(bg=COR_BOTAO, fg=COR_TEXTO,
                                 font=self.fonte_pequena, relief="flat",
                                 activebackground=COR_HOVER, highlightthickness=0)
        self._menu_portas["menu"].config(bg=COR_BOTAO, fg=COR_TEXTO)
        self._menu_portas.pack(side="left", padx=(0, 10))
        self._botao(porta_row, "Atualizar", self._atualizar_portas,
                    cor_bg="#222", fonte=self.fonte_pequena).pack(side="left")

        self._botao(self, "  COMEÇAR  ", self._iniciar_jogo,
                    cor_bg=COR_OURO, cor_fg="#1a1a2e",
                    fonte=self.fonte_grande).pack(pady=20, ipadx=10, ipady=4)

    def _atualizar_portas(self):
        portas = self._listar_portas()
        self._menu_portas["menu"].delete(0, "end")
        for p in portas:
            self._menu_portas["menu"].add_command(
                label=p, command=lambda v=p: self.porta_serial.set(v))
        if portas:
            self.porta_serial.set(portas[0])

    # ── Início ────────────────────────────────────────────────────────────────
    def _iniciar_jogo(self):
        porta = self.porta_serial.get()
        if porta and porta != "(nenhuma)":
            if not self._conectar_serial(porta):
                self._label(self, "⚠ Falha ao conectar. Verifique a porta.",
                            cor=COR_ERRADO, fonte=self.fonte_pequena).pack()
                return
        self.pontos    = [0, 0]
        self.perguntas = random.sample(PERGUNTAS, TOTAL_PERGUNTAS)
        self.q_index   = 0
        self._tela_buzzer()

    # ── Tela de Buzzer ────────────────────────────────────────────────────────
    def _tela_buzzer(self):
        self._limpar()
        self.aguardando_buzzer  = True
        self.respondendo        = False
        self.primeira_tentativa = True

        nomes = [self.nome_p1.get(), self.nome_p2.get()]
        q     = self.perguntas[self.q_index]

        hdr = tk.Frame(self, bg=COR_BG)
        hdr.pack(fill="x", padx=20, pady=(18, 6))
        self._label(hdr, f"Pergunta {self.q_index+1} de {TOTAL_PERGUNTAS}",
                    cor="#aaa", fonte=self.fonte_pequena).pack(side="left")
        self._label(hdr,
                    f"🔵 {nomes[0]}: {self.pontos[0]}   "
                    f"🔴 {nomes[1]}: {self.pontos[1]}",
                    cor="#aaa", fonte=self.fonte_pequena).pack(side="right")

        tk.Frame(self, bg=COR_BUZZER, height=3).pack(fill="x", padx=20)

        c = self._card(self, padx=24, pady=18)
        c.pack(fill="x", padx=20, pady=12)
        self._label(c, q["pergunta"], cor=COR_TITULO, fonte=self.fonte_grande,
                    wraplength=700, justify="center").pack()

        wait = tk.Frame(self, bg=COR_BG)
        wait.pack(pady=16)
        self._label(wait, "⚡  QUEM SABE?", cor=COR_BUZZER,
                    fonte=self.fonte_buzzer).pack()
        self._label(wait, "Aperte o botão no Arduino para responder!",
                    cor="#aaa", fonte=self.fonte_pequena).pack(pady=(4, 0))

        fallback = tk.Frame(self, bg=COR_BG)
        fallback.pack(pady=6)
        self._label(fallback, "Sem Arduino – clique abaixo:",
                    cor="#555", fonte=self.fonte_pequena).pack()
        btn_row = tk.Frame(fallback, bg=COR_BG)
        btn_row.pack(pady=6)
        self._botao(btn_row, f"🔵 {nomes[0]}  (F1)",
                    lambda: self._buzzer_ativado(0),
                    cor_bg="#0a3a6e", cor_fg=COR_P1).pack(side="left", padx=10,
                                                           ipadx=8, ipady=4)
        self._botao(btn_row, f"🔴 {nomes[1]}  (F2)",
                    lambda: self._buzzer_ativado(1),
                    cor_bg="#5a1a1a", cor_fg=COR_P2).pack(side="left", padx=10,
                                                           ipadx=8, ipady=4)

        self.bind("<F1>", lambda e: self._buzzer_ativado(0))
        self.bind("<F2>", lambda e: self._buzzer_ativado(1))
        self._enviar_serial("READY")

    # ── Buzzer ativado ────────────────────────────────────────────────────────
    def _buzzer_ativado(self, jogador):
        if not self.aguardando_buzzer:
            return
        self.aguardando_buzzer = False
        self.unbind("<F1>")
        self.unbind("<F2>")
        self.vez_atual = jogador
        self._tela_resposta()

    # ── Tela de resposta ──────────────────────────────────────────────────────
    def _tela_resposta(self, segunda_chance=False):
        self._limpar()
        self.respondendo = True

        nomes = [self.nome_p1.get(), self.nome_p2.get()]
        cor   = [COR_P1, COR_P2][self.vez_atual]
        emoji = ["🔵", "🔴"][self.vez_atual]
        q     = self.perguntas[self.q_index]

        anuncio = tk.Frame(self, bg=COR_BG)
        anuncio.pack(fill="x", pady=(16, 4))

        if segunda_chance:
            self._label(anuncio,
                        f"{emoji}  {nomes[self.vez_atual]} — segunda chance!",
                        cor=cor, fonte=self.fonte_grande).pack()
            self._label(anuncio, "O adversário errou. Você sabe a resposta?",
                        cor=COR_BUZZER, fonte=self.fonte_pequena).pack(pady=(2, 0))
        else:
            self._label(anuncio,
                        f"{emoji}  {nomes[self.vez_atual]} respondeu primeiro!",
                        cor=cor, fonte=self.fonte_grande).pack()
            self._label(anuncio, "Escolha a resposta correta:",
                        cor="#aaa", fonte=self.fonte_pequena).pack(pady=(2, 0))

        tk.Frame(self, bg=cor, height=3).pack(fill="x", padx=20)

        placar = tk.Frame(self, bg=COR_BG)
        placar.pack(fill="x", padx=20, pady=4)
        self._label(placar,
                    f"🔵 {nomes[0]}: {self.pontos[0]}   "
                    f"🔴 {nomes[1]}: {self.pontos[1]}",
                    cor="#666", fonte=self.fonte_pequena).pack(side="left")

        c = self._card(self, padx=24, pady=14)
        c.pack(fill="x", padx=20, pady=8)
        self._label(c, q["pergunta"], cor=COR_TITULO, fonte=self.fonte_grande,
                    wraplength=680, justify="center").pack()

        self.botoes_opcao = []
        for i, texto in enumerate(q["opcoes"]):
            letras = ["A", "B", "C", "D"]
            btn = self._botao(self, f"  {letras[i]})  {texto}  ",
                              lambda idx=i: self._responder(idx),
                              cor_bg=COR_BOTAO, anchor="w")
            btn.pack(fill="x", padx=20, pady=4, ipady=8)
            self.botoes_opcao.append(btn)

    # ── Processar resposta ────────────────────────────────────────────────────
    def _responder(self, idx_escolha):
        if not self.respondendo:
            return
        self.respondendo = False

        for btn in self.botoes_opcao:
            btn.config(state="disabled")

        q       = self.perguntas[self.q_index]
        correta = q["resposta"]
        acertou = (idx_escolha == correta)
        nomes   = [self.nome_p1.get(), self.nome_p2.get()]

        # Destaca resposta certa e errada
        self.botoes_opcao[correta].config(bg=COR_CERTO, fg="#1a1a2e")
        if not acertou:
            self.botoes_opcao[idx_escolha].config(bg=COR_ERRADO, fg="#1a1a2e")

        if acertou:
            # ✅ Acertou → ponto, próxima pergunta
            self.pontos[self.vez_atual] += 1
            msg     = f"✅  {nomes[self.vez_atual]} acertou! +1 ponto!"
            cor_msg = COR_CERTO
            self._enviar_serial("RESET")
            self.after(1800, self._proxima)

        elif self.primeira_tentativa:
            # ❌ Primeiro erro → adversário ganha a chance de responder
            self.primeira_tentativa = False
            adversario = 1 - self.vez_atual
            msg = (f"❌  {nomes[self.vez_atual]} errou!\n"
                   f"💡  {nomes[adversario]} tem a chance!")
            cor_msg = COR_ERRADO
            self._enviar_serial("RESET")
            self.vez_atual = adversario
            self.after(2200, lambda: self._tela_resposta(segunda_chance=True))

        else:
            # ❌ Adversário também errou → ninguém pontua
            msg     = "❌  Ninguém acertou! Próxima pergunta..."
            cor_msg = COR_ERRADO
            self._enviar_serial("RESET")
            self.after(2000, self._proxima)

        tk.Label(self, text=msg, bg=COR_BG, fg=cor_msg,
                 font=self.fonte_grande,
                 wraplength=680, justify="center").pack(pady=10)

    # ── Próxima ───────────────────────────────────────────────────────────────
    def _proxima(self):
        self.q_index += 1
        if self.q_index >= TOTAL_PERGUNTAS:
            self._tela_resultado()
        else:
            self._tela_buzzer()

    # ── Resultado ─────────────────────────────────────────────────────────────
    def _tela_resultado(self):
        self._limpar()
        nomes = [self.nome_p1.get(), self.nome_p2.get()]
        p1, p2 = self.pontos

        if p1 > p2:
            vencedor, cor_v = nomes[0], COR_P1
        elif p2 > p1:
            vencedor, cor_v = nomes[1], COR_P2
        else:
            vencedor, cor_v = "Empate!", COR_OURO

        tk.Frame(self, bg=COR_BG).pack(expand=True)
        self._label(self, "🏆  RESULTADO FINAL", cor=COR_OURO,
                    fonte=self.fonte_titulo).pack()

        c = self._card(self, padx=40, pady=24)
        c.pack(padx=60, pady=20)
        row = tk.Frame(c, bg=COR_CARD)
        row.pack()
        for nome, pts, cor, em in [(nomes[0], p1, COR_P1, "🔵"),
                                    (nomes[1], p2, COR_P2, "🔴")]:
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
        self._botao(btns, "  JOGAR NOVAMENTE  ", self._reiniciar,
                    cor_bg=COR_OURO, cor_fg="#1a1a2e",
                    fonte=self.fonte_grande).pack(side="left", padx=8,
                                                  ipadx=8, ipady=4)
        self._botao(btns, "  MENU INICIAL  ", self._voltar_menu,
                    cor_bg=COR_BOTAO).pack(side="left", padx=8,
                                           ipadx=8, ipady=4)
        tk.Frame(self, bg=COR_BG).pack(expand=True)

    def _reiniciar(self):
        self.pontos    = [0, 0]
        self.perguntas = random.sample(PERGUNTAS, TOTAL_PERGUNTAS)
        self.q_index   = 0
        self._tela_buzzer()

    def _voltar_menu(self):
        self._serial_running = False
        if self.serial_conn:
            try:
                self.serial_conn.close()
            except Exception:
                pass
            self.serial_conn = None
        self._tela_inicial()

    def destroy(self):
        self._serial_running = False
        super().destroy()


if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
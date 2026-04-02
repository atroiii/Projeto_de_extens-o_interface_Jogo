
import tkinter as tk
from tkinter import font as tkfont
from Service.quiz_logica import QuizModel


COR_TEXTO = "black"
COR_BOTAO = "#3498db"
COR_BG = "#ecf0f1"
COR_CERTO = "#2ecc71"  # verde para resposta correta
COR_ERRADO = "#e74c3c"  # vermelho para resposta errada
FONTE_PADRAO = ("Arial", 12)


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
    },
    {
    "nome": "Hacker",
    "BG": "#0a0a0a",      
    "CARD": "#141414",    
    "BOTAO": "#003b00",   
    "HOVER": "#008f11",  
    "TEXTO": "#00ff41",   
    "TITULO": "#ffffff",
    "OURO": "#adff2f",    
    "BUZZER": "#00ff41",
    "P1": "#00ff41",
    "P2": "#008f11",
    },
    {
    "nome": "Dracula",
    "BG": "#282a36",      
    "CARD": "#44475a",    
    "BOTAO": "#6272a4",  
    "HOVER": "#bd93f9",   
    "TEXTO": "#f8f8f2",   
    "TITULO": "#50fa7b",  
    "OURO": "#f1fa8c",    
    "BUZZER": "#ffb86c",  
    "P1": "#8be9fd",      
    "P2": "#ff79c6",    
    },
    {
    "nome": "Ocean",
    "BG": "#001219",      # Azul oceano profundo
    "CARD": "#005f73",    # Petróleo
    "BOTAO": "#0a9396",   # Turquesa médio
    "HOVER": "#94d2bd",   # Aquamarine claro
    "TEXTO": "#e9d8a6",   # Areia (bege claro)
    "TITULO": "#ffffff",
    "OURO": "#ee9b00",    # Laranja ensolarado
    "BUZZER": "#ae2012",  # Coral escuro
    "P1": "#94d2bd",      # Verde água
    "P2": "#e9d8a6",      # Creme
    },
    {
    "nome": "Cyberpunk",
    "BG": "#03001c",      # Roxo quase preto
    "CARD": "#301e67",    # Roxo profundo
    "BOTAO": "#5b8fb9",   # Azul metálico
    "HOVER": "#b6eada",   # Ciano neon
    "TEXTO": "#b6eada",   # Ciano claro
    "TITULO": "#ffffff",
    "OURO": "#ffee63",    # Amarelo choque
    "BUZZER": "#ff0054",  # Magenta/Rosa choque
    "P1": "#00f5d4",      # Turquesa neon
    "P2": "#9b5de5",      # Roxo vibrante
    },
    {
    "nome": "Forest",
    "BG": "#1a2f16",      # Verde floresta escuro
    "CARD": "#2d4a22",    # Verde musgo
    "BOTAO": "#606c38",   # Oliva
    "HOVER": "#a3b18a",   # Sálvia
    "TEXTO": "#fefae0",   # Marfim
    "TITULO": "#ffffff",
    "OURO": "#dda15e",    # Madeira clara
    "BUZZER": "#bc6c25",  # Terra/Castanho
    "P1": "#a3b18a",      # Verde pálido
    "P2": "#dda15e",      # Bege escuro
    },
    {
    "nome": "Contraste",
    "BG": "#000000",      # Preto puro
    "CARD": "#1a1a1a",    # Cinza escuro
    "BOTAO": "#ffffff",   # Branco puro
    "HOVER": "#ffff00",   # Amarelo puro
    "TEXTO": "#ffffff",   # Branco
    "TITULO": "#ffff00",  # Amarelo
    "OURO": "#ffff00",
    "BUZZER": "#ff0000",  # Vermelho puro
    "P1": "#ffffff",      # Branco
    "P2": "#ffff00",      # Amarelo
    }
]



class QuizUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz ")


        self.state("zoomed")


        self.resizable(True, True)

        self.configure(bg=COR_BG)

        self.tema_index = 0
        self._aplicar_tema()

        self.bind("<F1>", lambda e: self.model.acionar_buzzer_teclado(0))
        self.bind("<F2>", lambda e: self.model.acionar_buzzer_teclado(1))

        self.bind("<F11>", lambda e: self.attributes("-fullscreen", not self.attributes("-fullscreen")))

        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

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

    def _botao(self, master, texto, cmd, cor_bg=None,
            cor_fg=None, fonte=None, **kw):

        if fonte is None:
            fonte = self.fonte_opcao

        if cor_bg is None:
            cor_bg = COR_BOTAO

        if cor_fg is None:
            cor_fg = COR_TEXTO

        return tk.Button(master, text=texto, command=cmd,
                        bg=cor_bg, fg=cor_fg, font=fonte,
                        activebackground=COR_HOVER,
                        activeforeground=COR_TITULO,
                        relief="flat", cursor="hand2",
                        padx=10, pady=6, **kw)
    
    def _atualizar_portas(self):  
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

        COR_CERTO = "#2ecc71" 
        COR_ERRADO = "#e74c3c"

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

    def _exibir_historico_volatil(self):
        janela = tk.Toplevel(self)
        janela.title("Resultados da Sessão")
        janela.geometry("450x500")
        janela.configure(bg=COR_BG)

        self._label(janela, "📊 RESULTADOS ATUAIS", cor=COR_OURO, fonte=self.fonte_grande).pack(pady=20)

        if not self.model.historico_sessao:
            self._label(janela, "Nenhum jogo finalizado nesta sessão.", cor="#888").pack(pady=50)
            return

        container = tk.Frame(janela, bg=COR_BG)
        container.pack(fill="both", expand=True, padx=20)

        #Ordenacao
        for i, jogo in enumerate(reversed(self.model.historico_sessao)):
            card = self._card(container)
            card.pack(fill="x", pady=5, ipady=5)
            
            texto = f"JOGO {len(self.model.historico_sessao) - i}\n" \
                    f"{jogo['p1']['nome']} [{jogo['p1']['pontos']}] x [{jogo['p2']['pontos']}] {jogo['p2']['nome']}"
            
            self._label(card, texto, fonte=self.fonte_pequena).pack()
            self._label(card, f"Vencedor: {jogo['vencedor']}", cor=COR_OURO, fonte=self.fonte_pequena).pack()

    def _trocar_tema(self):
        self.tema_index = (self.tema_index + 1) % len(TEMAS)
        self._aplicar_tema()
        self._tela_inicial()

        #  Tela Inicial 
    
    def _tela_inicial(self):
        self._limpar()

        #TOPO 
        topo = tk.Frame(self, bg=COR_BG)
        topo.pack(fill="x", pady=30)

        self._label(topo, "🎯 QUIZ DOIS JOGADORES",
                    cor=COR_OURO, fonte=self.fonte_titulo).pack()

        self._label(topo, "10 perguntas · Quem errar passa a vez!",
                    cor=COR_TEXTO, fonte=self.fonte_pequena).pack(pady=10)

        #CONTEÚDO CENTRAL
        centro = tk.Frame(self, bg=COR_BG)
        centro.pack(expand=True)

        #Jogadores
        row_nomes = tk.Frame(centro, bg=COR_BG)
        row_nomes.pack(pady=30)

        for i, (var, cor) in enumerate([(self.nome_p1, COR_P1),
                                        (self.nome_p2, COR_P2)]):

            card = self._card(row_nomes, padx=40, pady=30)
            card.grid(row=0, column=i, padx=40)

            emoji = "🔵" if i == 0 else "🔴"

            self._label(card, f"{emoji} Jogador {i + 1}",
                        cor=cor, fonte=self.fonte_grande).pack()

            tk.Entry(card, textvariable=var,
                    font=self.fonte_media,
                    bg=COR_BOTAO, fg=COR_TITULO,
                    insertbackground=COR_TITULO,
                    relief="flat", justify="center",
                    width=20).pack(pady=15, ipady=10)

        #Arduino
        arduino_card = self._card(centro, padx=30, pady=20)
        arduino_card.pack(pady=20)

        self._label(arduino_card, "⚡ Conexão Arduino",
                    cor=COR_BUZZER, fonte=self.fonte_grande).pack()

        porta_row = tk.Frame(arduino_card, bg=COR_CARD)
        porta_row.pack(pady=10)

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

        #BOTÃO COMEÇAR 
        self._botao(self, "  COMEÇAR  ",
                    self._iniciar_jogo,
                    cor_bg=COR_OURO,
                    cor_fg="#1a1a2e",
                    fonte=self.fonte_grande).place(relx=0.50, rely=0.90, anchor="center")

        #BOTÃO TEMA
        self._botao(
            self,
            "🎨",
            self._trocar_tema,
            fonte=tkfont.Font(size=40)
        ).place(relx=0.98, rely=0.95, anchor="se", width=70, height=70)
        
        #BOTAO HISTORICO
        self._botao(self, "📊 PLACAR DA SESSÃO", 
            self._exibir_historico_volatil,
            cor_bg=COR_CARD, 
            fonte=self.fonte_pequena).place(relx=0.02, rely=0.95, anchor="sw")
        
    #fim tela inicial

    def _on_pergunta_carregada(self, **dados):
        """Exibe tela de buzzer com as alternativas como botões"""
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

        # Exibir alternativas como botões (desabilitados)
        self.botoes_opcao = []
        for i, texto in enumerate(dados['opcoes']):
            letras = ["A", "B", "C", "D"]
            btn = self._botao(self, f"  {letras[i]})  {texto}  ",
                              lambda idx=i: None,  # Desabilitado nesta fase
                              cor_bg=COR_BOTAO, anchor="w")
            btn.config(state="disabled")
            btn.pack(fill="x", padx=20, pady=4, ipady=8)
            self.botoes_opcao.append(btn)

        wait = tk.Frame(self, bg=COR_BG)
        wait.pack(pady=16)
        self._label(wait, "⚡  QUEM SABE?", cor=COR_BUZZER,
                    fonte=self.fonte_buzzer).pack()
        self._label(wait, "Aperte o botão no Arduino para responder!",
                    cor="#aaa", fonte=self.fonte_pequena).pack(pady=(4, 0))

    def _on_buzzer_ativado(self, **dados):
        """Exibe tela de resposta e ativa os botões"""
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

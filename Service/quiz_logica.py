
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
]

TOTAL_PERGUNTAS = 10


class SerialManager:

    def __init__(self, callback_buzzer=None):
        self.serial_conn = None
        self._running = False
        self.callback_buzzer = callback_buzzer

    def listar_portas(self):
        return [p.device for p in serial.tools.list_ports.comports()]

    def conectar(self, porta):
        try:
            self.serial_conn = serial.Serial(porta, BAUD_RATE, timeout=0.1)
            self._running = True
            threading.Thread(target=self._ler_serial, daemon=True).start()
            return True
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return False

    def _ler_serial(self):
        while self._running and self.serial_conn:
            try:
                if self.serial_conn.in_waiting:
                    linha = self.serial_conn.readline().decode("utf-8").strip()
                    if linha in ("1", "2") and self.callback_buzzer:
                        jogador = int(linha) - 1
                        self.callback_buzzer(jogador)
            except Exception:
                break

    def enviar(self, cmd):
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write((cmd + "\n").encode())
            except Exception:
                pass

    def desconectar(self):
        self._running = False
        if self.serial_conn:
            try:
                self.serial_conn.close()
            except Exception:
                pass
            self.serial_conn = None


class QuizModel:

    def __init__(self):
        self.nome_p1 = "Jogador 1"
        self.nome_p2 = "Jogador 2"

        self.pontos = [0, 0]
        self.perguntas = []
        self.q_index = 0
        self.vez_atual = 0

        self.primeira_tentativa = True
        self.respondendo = False
        self.aguardando_buzzer = False

        self.serial_manager = SerialManager(callback_buzzer=self._on_buzzer)

        self.callbacks = {
            'pergunta_carregada': None,
            'buzzer_ativado': None,
            'resposta_processada': None,
            'proximo': None,
            'jogo_finalizado': None,
        }

    def acionar_buzzer_teclado(self, jogador):
        self._on_buzzer(jogador)


    def registrar_callback(self, evento, func):
        if evento in self.callbacks:
            self.callbacks[evento] = func

    def _emitir(self, evento, **dados):
        if self.callbacks[evento]:
            self.callbacks[evento](**dados)

    def inicializar(self, nome_p1, nome_p2, porta_serial=None):
        self.nome_p1 = nome_p1
        self.nome_p2 = nome_p2
        self.pontos = [0, 0]
        self.perguntas = random.sample(PERGUNTAS, TOTAL_PERGUNTAS)
        self.q_index = 0

        if porta_serial:
            self.serial_manager.conectar(porta_serial)

        self._carregar_pergunta()

    def _carregar_pergunta(self):
        self.primeira_tentativa = True
        self.aguardando_buzzer = True
        self.respondendo = False

        q = self.perguntas[self.q_index]
        self._emitir('pergunta_carregada',
                     pergunta=q['pergunta'],
                     numero=self.q_index + 1,
                     total=TOTAL_PERGUNTAS,
                     nome_p1=self.nome_p1,
                     nome_p2=self.nome_p2,
                     pontos_p1=self.pontos[0],
                     pontos_p2=self.pontos[1])

        self.serial_manager.enviar("READY")

    # ── Buzzer ────────────────────────────────────────────────
    def _on_buzzer(self, jogador):
        if not self.aguardando_buzzer:
            return

        self.aguardando_buzzer = False
        self.vez_atual = jogador

        self._emitir('buzzer_ativado',
                     jogador=jogador,
                     nome=self.nome_p1 if jogador == 0 else self.nome_p2)

    # ── Resposta ──────────────────────────────────────────────
    def responder(self, idx_escolha):
        if not self.respondendo:
            return

        self.respondendo = False

        q = self.perguntas[self.q_index]
        correta = q['resposta']
        acertou = (idx_escolha == correta)

        resultado = {
            'acertou': acertou,
            'resposta_correta': correta,
            'resposta_escolhida': idx_escolha,
            'jogador': self.vez_atual,
            'nome': self.nome_p1 if self.vez_atual == 0 else self.nome_p2,
            'nome_adversario': self.nome_p2 if self.vez_atual == 0 else self.nome_p1,
        }

        if acertou:
            self.pontos[self.vez_atual] += 1
            resultado['acao'] = 'proximo'
            resultado['msg'] = f"✅  {resultado['nome']} acertou! +1 ponto!"
            self.serial_manager.enviar("RESET")

        elif self.primeira_tentativa:
            self.primeira_tentativa = False
            adversario = 1 - self.vez_atual
            resultado['acao'] = 'segunda_chance'
            resultado['proximo_jogador'] = adversario
            resultado['msg'] = (f"❌  {resultado['nome']} errou!\n"
                                f"💡  {resultado['nome_adversario']} tem a chance!")
            self.serial_manager.enviar("RESET")

        else:
            resultado['acao'] = 'proximo'
            resultado['msg'] = "❌  Ninguém acertou! Próxima pergunta..."
            self.serial_manager.enviar("RESET")

        self._emitir('resposta_processada', **resultado)

    def proxima_pergunta(self):
        self.q_index += 1

        if self.q_index >= TOTAL_PERGUNTAS:
            self._emitir('jogo_finalizado',
                         nome_p1=self.nome_p1,
                         nome_p2=self.nome_p2,
                         pontos_p1=self.pontos[0],
                         pontos_p2=self.pontos[1])
        else:
            self._carregar_pergunta()

    def reiniciar(self):
        self.pontos = [0, 0]
        self.perguntas = random.sample(PERGUNTAS, TOTAL_PERGUNTAS)
        self.q_index = 0
        self._carregar_pergunta()

    def encerrar(self):
        self.serial_manager.desconectar()


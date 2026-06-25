<div align="center">

# 🎮 Tech Quiz

### Quiz interativo com integração Arduino — projeto de extensão universitária

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Arduino](https://img.shields.io/badge/Arduino-C%2FC%2B%2B-00979D?style=for-the-badge&logo=arduino&logoColor=white)](https://www.arduino.cc/)
[![Tkinter](https://img.shields.io/badge/Interface-Tkinter-FF6F00?style=for-the-badge)](https://docs.python.org/3/library/tkinter.html)


</div>

---

## 📖 Sobre o projeto

O **Tech Quiz** nasceu como um projeto de extensão universitária. A proposta inicial era simples: desenvolver apenas uma interface gráfica. Nosso grupo foi além — criamos um jogo de quiz completo com **integração física via Arduino**, conectando hardware e software em uma experiência interativa e divertida.

O jogo suporta dois jogadores que competem em tempo real usando **buzzers físicos** conectados ao Arduino. Quando um jogador pressiona o buzzer, o Arduino envia uma string serial ao Python, que identifica o jogador e processa a resposta. A interface, desenvolvida em **Tkinter**, exibe perguntas, placar e histórico de partidas — tudo com suporte a temas visuais e múltiplos modos de tela.

---

## Menu:
![alt](<screenshots/menu.png>)

### Questão
![alt](<screenshots/tela_inicial.png>)

### Acerto
![alt](<screenshots/acertou.png>)

### End
![alt](<screenshots/resultado_final.png>)

### Histórico:
![alt](<screenshots/resultado.png>)


## ✨ Funcionalidades

- 🎯 **Modo dois jogadores** com buzzers físicos
- 🔌 **Integração serial com Arduino** 
- 🖥️ **Interface gráfica** completa em Tkinter com suporte a temas claro/escuro
- 📊 **Histórico de partidas**
- ⚙️ **Configurações dinâmicas**
- 🏆 **Sistema de pontuação** 

---

## 🔌 Como funciona a integração com o Arduino

```
[ Jogador aperta o buzzer ]
        │
        ▼
[ Arduino detecta o sinal ]
        │
        ▼
[ Arduino envia string serial → ex: "1" ou "2" ]
        │
        ▼
[ Python lê a porta serial via SerialManager ]
        │
        ▼
[ QuestionarioModelo processa quem apertou ]
        │
        ▼
[ QuizUI atualiza a interface em tempo real ]
```

O código do Arduino (`buzzer.ino`) monitora dois botões físicos e envia `"1"` ou `"2"` pela porta serial quando detecta um acionamento. O Python lê essa string e dispara o evento correspondente no modelo do jogo.

---

## 🧩 Arquitetura de componentes

### `QuestionarioModelo` — Núcleo do jogo

Gerencia toda a lógica de partida, comunicação com o Arduino e disparo de eventos.

| Atributo | Tipo | Descrição |
|---|---|---|
| `nomes_jogadores` | `str` | Nomes dos jogadores (P1 e P2) |
| `pontos_jogador` | `list[int, int]` | Placar atual |
| `question_index` | `int` | Índice da pergunta atual |
| `current_player` | `int` | Jogador com vez |
| `primeira_tentativa` | `bool` | Indica se é a primeira tentativa |
| `is_waiting_buzzer` | `bool` | Aguardando acionamento do buzzer |
| `historico_sessao` | `list[Jogo]` | Histórico de partidas |

**Callbacks disponíveis:**

| Evento | Descrição |
|---|---|
| `on_question_loaded` | Disparado ao carregar nova pergunta |
| `buzzer_activator` | Disparado ao detectar acionamento do buzzer |
| `on_answer_processed` | Disparado após processar a resposta |
| `on_next_question` | Disparado ao avançar de pergunta |
| `on_game_finished` | Disparado ao fim da partida |

---

### `SerialManager` — Comunicação com o Arduino

| Método | Retorno | Descrição |
|---|---|---|
| `lista_portas()` | `list` | Lista portas seriais disponíveis |
| `conectar(porta)` | `bool` | Conecta à porta especificada |
| `ler()` | — | Lê dados recebidos do Arduino |
| `enviar(cmd)` | — | Envia comando ao Arduino |
| `desconectar()` | — | Encerra a conexão |

---

### `QuizUI` — Interface gráfica (Tkinter)

Responsável por toda a camada visual do jogo.

- Gerenciamento de fontes: `título`, `grande`, `mediana`, `pequeno`, `escolha`, `campainha`
- Telas: menu principal, jogo, tentativa novamente, histórico
- Suporte a temas com aplicação e troca em tempo de execução
- Registro automático dos callbacks do modelo

---

## 🚀 Como rodar o projeto

### Pré-requisitos

- Python 3.10 ou superior
- Biblioteca `pyserial`

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/tech-quiz.git
cd tech-quiz
```

### 2. Instale as dependências Python

```bash
pip install pyserial
```

### 3. Grave o código no Arduino

Abra o arquivo `arduino/buzzer.ino` na Arduino IDE, selecione a placa e a porta corretas e clique em **Carregar**.

### 4. Monte o circuito

Conecte dois botões (buzzers) ao Arduino:

| Botão | Pino Arduino | Leds    | 
|---|--------------|---------|
| Jogador 1 | Pino 2       | Pino 3  |
| Jogador 2 | Pino 13      | Pino 12 |



### 5. Execute o jogo

```bash
python main.py
```

Na tela de configurações, selecione a porta serial do Arduino, insira os nomes dos jogadores e clique em **Iniciar**.

---

## 🎮 Como jogar

1. Conecte o Arduino ao computador
2. Abra o jogo e configure os nomes e a porta serial
3. O jogo exibe uma pergunta com alternativas na tela
4. O primeiro jogador a apertar o buzzer ganha o direito de responder
5. Resposta correta → ponto; resposta errada → o outro jogador tenta
6. Ao fim de todas as perguntas, o vencedor é exibido com o histórico da partida

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3 | Lógica do jogo e interface |
| Tkinter | Interface gráfica |
| pyserial | Comunicação com o Arduino |
| C/C++ (Arduino) | Detecção dos buzzers e envio serial |

---

## 📄 Licença


| Asset | Autor | Licença |
|---|---|---|
| Press Start 2P (fonte) | © 2012 The Press Start 2P Project Authors (cody@zone38.net) | SIL Open Font License 1.1  |
| Tiny Dungeon 1.0 (sprites) | © 2022 Kenney (kenney.nl) | CC0 1.0 Universal  |


---



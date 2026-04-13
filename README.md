# Projeto de Extensão interface de um Jogo
 * versão 1.0.0v

## Menu:
![alt](<screenshots/Captura de tela de 2026-04-13 13-29-31.png>)

### Histórico:
![alt](<screenshots/Captura de tela de 2026-04-13 14-44-01.png>)

## Gameplay:
![alt](<screenshots/Captura de tela de 2026-04-13 14-41-16.png>)

### Questão
![alt](<screenshots/Captura de tela de 2026-04-13 14-41-22.png>)

### Empate
![alt](<screenshots/Captura de tela de 2026-04-13 14-41-33.png>)

### Acerto
![alt](<screenshots/Captura de tela de 2026-04-13 14-42-43.png>)

### End
![alt](<screenshots/Captura de tela de 2026-04-13 14-43-37.png>)


## Componentes:
 * Theme:
    * themesdata
 * Settings
 * QuizGame
 * QuizFont
 * Emulator
 * Callback
 * QuizUI
 * QuizModel
    * dataset


## Project structure ARD 20260411
main : entry point

Settings
Callbacks:
 * on\_question\_loaded
 * on\_buzzer\_activated
 * on\_answer\_processed
 * on\_next_question
 * on\_game_finished

SerialManager:
 * init:
    * serial_connection: Serial
    * isrunning: bool
    * callback_buzzer: Callable

 * ports\_list() -> list
 * connect(port) -> bool
 * read()
 * send(cmd)
 * disconect()

Game:
 * players names
 * players points
 * winner

QuizModel:
 * init:
     * players names: str
         * p1, p2
     * player points: list[int, int]
     * questions: list[?]
     * question\_index: int
     * current_player \[vez atual\]: int
       
     * first_try: bool
     * is_answering: bool
     * is_waiting_buzzer: bool
     
     * session_history: list[Game]
     * SerialManager
     * callbacks: list
 * buzzer_activate(player)
 * register_end_of_game
 * register_callback(event: int, func)
 * emit(event, **data)
 * initialize(
        players name: str,
        serial_port: int
    )
 * question:
     * load()
     * next()
 * on_buzzer
 * answer(choice_index)
 * restart
 * finish

Fonts:
 * title
 * big
 * median
 * small
 * choice
 * buzzer

QuizUI(Tk):
 * init:
     * window settings
     * key binds:
         * F1, F2, F11, ESC
     * Fonts
     * player names
         * p1, p2
     * serial port
     * QuizModel
     * callbacks\_reg:
         * on\_question\_loaded
         * on\_buzzer\_activated
         * on\_answer\_processed
         * on\_game_finished

     * update_menu
     * clear
     * create:
         * card
         * label
         * button
     * ports_update
     * game_init
     * theme:
         * apply
         * change
     * history_show
     * screen:
         * menu
         * try_again
     * back_to_menu
     * destroy

## Changes
 * Uso de singletons

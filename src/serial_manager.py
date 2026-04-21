"""Serial Manager — conexão real com Arduino."""

from settings import Settings
import serial
import serial.tools.list_ports
import threading
import time


class SerialManager:
    connected_port = None

    @staticmethod
    def ports_list(model=None) -> list[str]:
        return [p.device for p in serial.tools.list_ports.comports()]

    @staticmethod
    def connect(model, port: str) -> None:
        try:
            model.serial_conn = serial.Serial(
                port, Settings.BAUD_RATE, timeout=0.1
            )
            model.running = True
            threading.Thread(target=SerialManager.read, args=(model,), daemon=True).start()
            SerialManager.connected_port = port
        except serial.SerialException as e:
            print(f"Erro ao conectar na porta {port}: {e}")
            model.running = False

    @staticmethod
    def disconnect(model) -> None:
        model.running = False
        if model.serial_conn is not None:
            try:
                model.serial_conn.close()
            except Exception:
                pass
            model.serial_conn = None

    @staticmethod
    def read(model) -> None:
        while model.running and (serial_conn := model.serial_conn) is not None:
            try:
                if serial_conn.in_waiting:
                    linha = serial_conn.readline().decode("utf-8").strip()
                    # Arduino manda "1" ou "2" para indicar qual buzzer foi apertado
                    if linha in ("1", "2") and model.callback_buzzer is not None:
                        jogador = int(linha) - 1
                        model.callback_buzzer(jogador)
            except serial.SerialException as e:
                print(f"Erro de leitura serial: {e}")
                break
            time.sleep(Settings.THREAD_DELAY)

    @staticmethod
    def send(model, cmd: str) -> None:
        if model.serial_conn and model.serial_conn.is_open:
            try:
                model.serial_conn.write((cmd + "\n").encode())
            except serial.SerialException:
                pass
"""Docs."""

from settings import Settings
from typing import Any
from dataclasses import dataclass
from random import randint, choice
import threading


@dataclass(frozen=True, slots=True)
class EmuPortInfo:
    device: str
    name: str
    description: str
    hwid: str
    vid: int
    pid: int
    serial_number: str
    manufacturer: str

    def __repr__(self) -> str:
        return self.name


@dataclass(frozen=True, slots=True)
class EmuSerial:
    port: EmuPortInfo
    baudrate: int = 9600
    bytesize: int = 0
    parity: int = 0
    stopbits: int = 0
    timeout: float = 1
    write_timeout: int = 2

    is_open: bool = True
    in_waiting: bool = True

    def readline(self) -> bytes:
        return choice(("1", "2")).encode("utf-8")

    def close(self) -> None: ...


def gen_random_port_list(n: int = 10) -> list[EmuPortInfo]:
    return [
        EmuPortInfo(
            f"/dev/ttyUSB{i}",
            f"ttyUSB{i}",
            "emulated device",
            "USB",
            randint(0, 2000),
            randint(0, 2000),
            hex(randint(0, 2000)),
            "emu",
        )
        for i in range(n)
    ]


class Emulator:
    connected_port = None

    @staticmethod
    def ports_list(model) -> list[EmuPortInfo]:
        return gen_random_port_list(10)

    @staticmethod
    def connect(model, port):
        Emulator.connected_port = port

        model.serial_conn = EmuSerial(port, Settings.BAUD_RATE, timeout=0.1)
        model.running = True
        threading.Thread(target=model.read, daemon=True).start()

    @staticmethod
    def disconnect(model):
        model.running = False
        if model.serial_conn is not None:
            try:
                model.serial_conn.close()
            except Exception:
                pass
            model.serial_conn = None

    @staticmethod
    def read(model) -> Any:
        print("in")
        while model.running and model.serial_conn is not None:
            if not model.serial_conn.in_waiting:
                continue
            linha = model.serial_conn.readline().decode("utf-8").strip()
            if linha in ("1", "2") and model.callback_buzzer is not None:
                jogador = int(linha) - 1
                model.callback_buzzer(jogador)
        print("out")

    @staticmethod
    def send(model, cmd) -> Any:
        if model.serial_conn and model.serial_conn.is_open:
            try:
                model.serial_conn.write((cmd + "\n").encode())
            except Exception:
                pass


if __name__ == "__main__":
    print(gen_random_port_list(10))

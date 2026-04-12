"""Docs."""

from typing import Any

from typing import Callable
from callback import Callback


class SerialManager:
    @staticmethod
    def init() -> bool:
        return True
    
    @staticmethod
    def ports_list() -> list:
        print("WARNING: SerialManager.port_list")
        return []
    
    @staticmethod
    def connect(port) -> bool:
        print("WARNING: SerialManager.connect")
        return True
    
    @staticmethod
    def disconnect() -> Any:
        print("WARNING: SerialManager.disconnect")
    
    @staticmethod
    def read() -> Any:
        print("WARNING: SerialManager.read")
    
    @staticmethod
    def send(cmd: Any) -> Any:
        print("WARNING: SerialManager.send")

        


class QuizModel:
    callbacks: dict[Callback, Callable | None] = {}

    @staticmethod
    def buzzer_activate(player) -> None:
        raise NotImplementedError("ERROR: buzzer_activate")

    @staticmethod
    def register_callback(event: Callback, func: Callable) -> None:
        """Docs."""

        assert event not in QuizModel.callbacks, "ERROR: Event already registed"
        QuizModel.callbacks[event] = func

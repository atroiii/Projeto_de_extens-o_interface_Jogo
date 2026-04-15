"""Docs."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Player:
    name: str
    points: int


@dataclass(frozen=True, slots=True)
class QuizGame:
    player_1: Player
    player_2: Player

    winner: int = -1

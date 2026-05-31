
from __future__ import annotations
from abc import ABC
import arcade

class Entidad(arcade.Sprite, ABC):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.eliminado: bool = False

    def on_collide(self, entidad: Entidad) -> None:
        pass

class Mob(Entidad):
    def __init__(self, hp: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._hp: int = hp
        self._muerto: bool = False

    def dañar(self) -> None:
        self._hp -= 1
        if self._hp <= 0:
            self._muerto = True

    @property
    def esta_muerto(self) -> bool:
        return self._muerto

from abc import ABC
import arcade

class Mob(arcade.Sprite, ABC):
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
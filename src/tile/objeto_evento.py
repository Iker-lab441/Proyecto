from typing import Callable, List

import arcade


class ObjetoEvento(arcade.Sprite):
    def __init__(self, interaccion1: List[Callable[[], None]], interaccion2: List[Callable[[], None]], path_or_texture = None, scale = 1, center_x = 0, center_y = 0, angle = 0, **kwargs):
        super().__init__(path_or_texture, scale, center_x, center_y, angle, **kwargs)
        self._interaccion1: List[Callable[[], None]] = interaccion1
        self._interaccion2: List[Callable[[], None]] = interaccion2
    
    @property
    def interaccion1(self) -> None:
        for funct in self._interaccion1:
            funct()

    @property
    def interaccion2(self) -> None:
        for funct in self._interaccion2:
            funct()
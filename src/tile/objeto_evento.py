from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, List

import arcade

from entidad.entidad import Entidad


class ObjetoEvento(Entidad, ABC):
    @abstractmethod
    def __init__(self, interaccion1: List[Callable[..., None]], interaccion2: List[Callable[..., None]],
                 texture: arcade.Texture | Path, scale: float, center_x: float, center_y: float, angle: float) -> None:
        super().__init__(texture, scale, center_x, center_y, angle)

        self._interaccion1: List[Callable[..., None]] = interaccion1
        self._interaccion2: List[Callable[..., None]] = interaccion2

    def interaccion1(self) -> None:
        for funct in self._interaccion1:
            funct()

    def interaccion2(self) -> None:
        for funct in self._interaccion2:
            funct()

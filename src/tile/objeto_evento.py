from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable

import arcade


class ObjetoEvento(arcade.Sprite, ABC):
    @abstractmethod
    def __init__(self, interaccion1: Callable[..., None], interaccion2: Callable[..., None],
                 path_or_texture: Path | None, scale: float = 1, center_x: float = 0, center_y: float = 0, angle: float = 0):
        super().__init__(path_or_texture, scale, center_x, center_y, angle)
        self._interaccion1: Callable[..., None] = interaccion1
        self._interaccion2: Callable[..., None] = interaccion2
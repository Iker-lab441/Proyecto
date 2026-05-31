#entidad
from abc import ABC, abstractmethod
from pathlib import Path

import arcade

class Entidad(arcade.Sprite, ABC):
    @abstractmethod
    def __init__(self, texture: arcade.Texture | Path, scale: float, center_x: float, center_y: float, angle: float = 0) -> None:
        super().__init__(texture, scale, center_x, center_y, angle)

    def on_collide(self, entidad: "Entidad") -> None:
        pass

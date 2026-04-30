from typing import Callable
from pathlib import Path

import arcade

import util.io
from objeto_evento import ObjetoEvento


class Palanca(ObjetoEvento):
    _SCALE: int = 1
    _PATH1: Path = Path("assets") / "images" / "palanca1.png"
    _PATH2: Path = Path("assets") / "images" / "palanca2.png"

    def __init__(self, interaccion1: Callable[[]], interaccion2: Callable[[]], center_x=0, center_y=0, angle=0, **kwargs) -> None:
        super().__init__(interaccion1, interaccion2, self._PATH1, self._SCALE, center_x, center_y, angle, **kwargs)
        self._activada: bool = False

        textura2 = arcade.texture.default_texture_cache.load_or_get_texture(self._PATH2)
        self.append_texture(textura2)

    def update(self, delta_time: float) -> None:
        if util.io.tecla_justo_pulsada(arcade.key.ENTER): # TODO: detectar colisión con el jugador
            self._interaccion1() if self._activada else self._interaccion2()
            self._toggle_activada()

    def _toggle_activada(self) -> None:
        self._activada = not self._activada
        self.set_texture(int(self._activada))
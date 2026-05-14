from typing import Callable
from pathlib import Path

import sys
import os

# Obtiene la ruta de 'proyecto/src' (subiendo un nivel desde 'proyecto/src/tile')
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if src_path not in sys.path:
    sys.path.append(src_path)

# Ahora puedes importar util.io
from util import io

import arcade

import config.controles as controles
from objeto_evento import ObjetoEvento
from entidad.jugador import Jugador


class Palanca(ObjetoEvento):
    _SCALE: int = 1
    _PATH1: Path = Path("assets") / "images" / "palanca1.png"
    _PATH2: Path = Path("assets") / "images" / "palanca2.png"

    def __init__(self, interaccion1: Callable[[]], interaccion2: Callable[[]], center_x=0, center_y=0, angle=0, **kwargs) -> None:
        super().__init__(interaccion1, interaccion2, self._PATH1, self._SCALE, center_x, center_y, angle, **kwargs)
        self._activada: bool = False

        textura2 = arcade.texture.default_texture_cache.load_or_get_texture(self._PATH2)
        self.append_texture(textura2)

    def on_collide(self, entidad: arcade.Sprite) -> None:
        if not isinstance(entidad, Jugador):
            return

        if io.tecla_justo_pulsada(controles.palanca_interactuar):
            self._interaccion1() if self._activada else self._interaccion2()
            self._toggle_activada()

    def _toggle_activada(self) -> None:
        self._activada = not self._activada
        self.set_texture(int(self._activada))
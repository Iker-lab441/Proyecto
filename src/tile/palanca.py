from typing import Callable, List
from pathlib import Path

import arcade


from util import io, texturas
import config.controles as controles
from tile.objeto_evento import ObjetoEvento
from entidad.jugador import Jugador


class Palanca(ObjetoEvento):
    _PATH1: Path = Path("assets") / "images" / "palanca1.png"
    _PATH2: Path = Path("assets") / "images" / "palanca2.png"

    def __init__(self, interaccion1: List[Callable[..., None]], interaccion2: List[Callable[..., None]], scale:float = 1, center_x=0, center_y=0, angle=0, **kwargs) -> None:
        super().__init__(interaccion1, interaccion2, texturas.Tiles.PALANCA1, scale, center_x, center_y, angle, **kwargs)
        self._activada: bool = False

        textura2 = arcade.texture.default_texture_cache.load_or_get_texture(self._PATH2)
        self.append_texture(textura2)

    def on_collide(self, entidad: arcade.Sprite) -> None:
        if not isinstance(entidad, Jugador):
            return

        if io.tecla_justo_pulsada(controles.palanca_interactuar):
            self._toggle_activada()
            self.interaccion1() if self._activada else self.interaccion2()

    def _toggle_activada(self) -> None:
        self._activada = not self._activada
        self.set_texture(int(self._activada))
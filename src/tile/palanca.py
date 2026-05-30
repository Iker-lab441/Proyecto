from typing import Callable, List
from pathlib import Path

import sys
import os


src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if src_path not in sys.path:
    sys.path.append(src_path)


from util import io
import arcade
import config.controles as controles
from tile.objeto_evento import ObjetoEvento
from entidad.jugador import Jugador


class Palanca(ObjetoEvento):
    _PATH1: Path = Path("assets") / "images" / "palanca1.png"
    _PATH2: Path = Path("assets") / "images" / "palanca2.png"

    def __init__(self, interaccion1: List[Callable[[], None]], interaccion2: List[Callable[[], None]], 
            tiempo_desactivacion: float = 3.0, scale:float = 1, center_x=0, center_y=0, angle=0, **kwargs) -> None:
        super().__init__(interaccion1, interaccion2, self._PATH1, scale, center_x, center_y, angle, **kwargs)
        
        self._activada: bool = False
        self._tiempo_desactivacion: float = tiempo_desactivacion
        self._tiempo_restante: float = 0.0

        textura2 = arcade.texture.default_texture_cache.load_or_get_texture(self._PATH2)
        self.append_texture(textura2)

    def on_collide(self, entidad: arcade.Sprite) -> None:
        if not isinstance(entidad, Jugador):
            return

        if io.tecla_justo_pulsada(controles.palanca_interactuar):
            self.activar_palanca()
    
    def activar_palanca(self) -> None:
        self._tiempo_restante = self._tiempo_desactivacion

        if not self._activada:
            self._activada = True
            self.set_texture(1)
            self._interaccion1()
    
    def on_update(self, delta_time: float = 1/60) -> None:
        if self._activada:
            self._tiempo_restante -= delta_time
            
            # Si se acaba el tiempo la soltamos
            if self._tiempo_restante <= 0:
                self.desactivar_palanca()

    def desactivar_palanca(self) -> None:
        self._activada = False
        self.set_texture(0)
        self._interaccion2()
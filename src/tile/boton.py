from typing import Callable
from pathlib import Path
import sys
import os


src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if src_path not in sys.path:
    sys.path.append(src_path)

import arcade
from objeto_evento import ObjetoEvento
from entidad.jugador import Jugador


class Boton(ObjetoEvento):
    _SCALE: int = 1
    def __init__(self, color: str, interaccion_pulsar: Callable[..., None], interaccion_soltar: Callable[..., None],
                 center_x: float = 0, center_y: float = 0, angle: float = 0) -> None:
        path_normal = Path("assets") / "images" / f"boton_{color}_normal.png"
        path_pulsado = Path("assets") / "images" / f"boton_{color}_pulsado.png"

        super().__init__([interaccion_pulsar], [interaccion_soltar], path_normal, self._SCALE, center_x, center_y, angle)

        self._pulsado: bool = False
        self._colisionando_este_frame: bool = False

        textura_pulsado = arcade.texture.default_texture_cache.load_or_get_texture(path_pulsado)
        self.append_texture(textura_pulsado)

    def on_collide(self, entidad: arcade.Sprite) -> None:
        if not isinstance(entidad, Jugador):
            return

        # Si hay colision
        self._colisionando_este_frame = True

        if not self._pulsado:
            self._activar_boton()
        
    def _activar_boton(self) -> None:
        self._pulsado = True
        self.set_texture(1)
        self.interaccion1()
        self._interaccion1()
        from util import globales
        globales.audio.reproducir("boton", volumen=0.5)
            
    def on_update(self, delta_time: float = 1/60) -> None:
        if self._pulsado and not self._colisionando_este_frame:
            self._desactivar_boton()
            
        self._colisionando_este_frame = False
        
    def _desactivar_boton(self) -> None:
        self._pulsado = False
        self.set_texture(0)
        self.interaccion2()
        self._interaccion2()
        from util import globales
        globales.audio.reproducir("boton", volumen=0.3)
    
    

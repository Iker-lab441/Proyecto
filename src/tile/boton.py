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

class Boton(ObjetoEvento):
    _SCALE: int = 1
    def __init__(self, color: str, interaccion_pulsar: Callable[[], None], interaccion_soltar: Callable[[], None], tiempo_desactivacion: float = 2.0, center_x = 0, center_y = 0, angle = 0, **kwargs) -> None:
        path_normal = Path("assets") / "images" / f"boton_{color}_normal.png"
        path_pulsado = Path("assets") / "images" / f"boton_{color}_pulsado.png"

        super().__init__(interaccion_pulsar, interaccion_soltar, path_normal, self._SCALE, center_x, center_y, angle, **kwargs)

        self._pulsado: bool = False
        self._tiempo_desactivacion: float = tiempo_desactivacion
        self._tiempo_restante: float = 0.0

        textura_pulsado = arcade.texture.default_texture_cache.load_or_get_texture(path_pulsado)
        self.append_texture(textura_pulsado)

    def on_collide(self, entidad: arcade.Sprite) -> None:
        if not isinstance(entidad, Jugador):
            return

        # Si el jugador pulsa la tecla de interactuar
        if io.tecla_justo_pulsada(controles.palanca_interactuar):
            self._activar_boton()
        
    def _activar_boton(self) -> None:
            self._tiempo_restante = self._tiempo_desactivacion
            # Si el botón no estaba pulsado ya, lo activamos
            if not self._pulsado:
                self._pulsado = True
                self.set_texture(1)
                self._interaccion1()
            
    def on_update(self, delta_time: float = 1/60) -> None:
        # Si el botón está pulsado, el temporizador empieza a bajar
            if self._pulsado:
                self._tiempo_restante -= delta_time
            
            # Si el tiempo se agota, desactivamos el botón
            if self._tiempo_restante <= 0:
                self._desactivar_boton()
    def _desactivar_boton(self) -> None:
            self._pulsado = False
            self.set_texture(0)
            self._interaccion2()
    
    

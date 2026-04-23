import arcade
import util.io
from objeto_evento import ObjetoEvento


class Palanca(ObjetoEvento):
    _SCALE: float = 1.0

    def __init__(self, interaccion1: function, interaccion2: function, center_x=0, center_y=0, angle=0, **kwargs):
        super().__init__(interaccion1, interaccion2, None, self._SCALE, center_x, center_y, angle, **kwargs)
        self._activada: bool = False

    def update(self, delta_time: float):
        if util.io.tecla_justo_pulsada(arcade.key.ENTER): # TODO: detectar colisión con el jugador
            self._interaccion1() if self._activada else self._interaccion2()
            self._activada = not self._activada
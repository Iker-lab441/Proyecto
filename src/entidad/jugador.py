import arcade

import util.io
import config.controles as controles


class Jugador(arcade.Sprite):
    _VELOCIDAD: float = 400.0

    def __init__(self, center_x: float, center_y: float):
        super().__init__(None, 1, center_x, center_y)

    def update(self, delta_time: float):
        super().update(delta_time)

        self.change_x = 0

        if util.io.tecla_mantenida(controles.jugador_izquierda):
            self.change_x -= self._VELOCIDAD * delta_time

        if util.io.tecla_mantenida(controles.jugador_derecha):
            self.change_x += self._VELOCIDAD * delta_time
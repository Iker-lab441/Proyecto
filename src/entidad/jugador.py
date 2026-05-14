import arcade

import util.io
import config.controles as controles


class Jugador(arcade.Sprite):
    _VELOCIDAD: float = 400.0
    _HP: int = 3

    def __init__(self, center_x: float, center_y: float):
        super().__init__(None, 1, center_x, center_y)

        self._hp: int = self._HP
        self._muerto: bool = False

    def update(self, delta_time: float):
        super().update(delta_time)

        self.change_x = 0

        if util.io.tecla_mantenida(controles.jugador_izquierda):
            self.change_x -= self._VELOCIDAD * delta_time

        if util.io.tecla_mantenida(controles.jugador_derecha):
            self.change_x += self._VELOCIDAD * delta_time

    def dañar(self) -> None:
        self._hp -= 1
        if self._hp == 0:
            self._muerto = True

    @property
    def esta_muerto(self) -> bool:
        return self._muerto
from pathlib import Path
import arcade

import util.io
import util.texturas as texturas
import config.controles as controles


class Jugador(arcade.Sprite):
    _VELOCIDAD: float = 400.0
    _HP: int = 3
    _FRAMES_PER_ANIM: int = 10

    def __init__(self, center_x: float, center_y: float) -> None:
        super().__init__(None, 1, center_x, center_y)

        self.texturas_andar: list[arcade.Texture] = texturas.Jugador.RUN
        self.texturas_saltar: list[arcade.Texture] = texturas.Jugador.JUMP

        self._en_suelo: bool = True

        self._hp: int = self._HP
        self._muerto: bool = False

    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        self._andar(delta_time)
        self._saltar()
        print(self.center_x, self.center_y)

    def _andar(self, delta_time: float) -> None:
        change_x_anterior: int = self.change_x
        self.change_x = 0

        if util.io.tecla_mantenida(controles.jugador_izquierda):
            self.change_x -= self._VELOCIDAD * delta_time

        if util.io.tecla_mantenida(controles.jugador_derecha):
            self.change_x += self._VELOCIDAD * delta_time

        # Las animaciones de salto tienen prioridad ante las de andar
        if not self.en_suelo:
            return

        # Si ha cambiado el signo o si está quieto
        if self.change_x * change_x_anterior <= 0:
            self.cur_texture = 0
            if self.change_x != 0:
                self.scale_x = util.signo(self.change_x) * abs(self.scale_x)
        else:
            self.cur_texture = (self.cur_texture + 1) % (len(self.texturas_andar) * self._FRAMES_PER_ANIM)

        self.texture = self.texturas_andar[self.cur_texture // self._FRAMES_PER_ANIM]

    def _saltar(self) -> None:
        if self.change_y > 0:
            self.texture = self.texturas_saltar[self.cur_texture]

    def dañar(self) -> None:
        self._hp -= 1
        if self._hp == 0:
            self._muerto = True

    @property
    def esta_muerto(self) -> bool:
        return self._muerto

    @property
    def en_suelo(self) -> bool:
        return self._en_suelo

    @en_suelo.setter
    def en_suelo(self, valor: bool) -> None:
        self._en_suelo = valor
    
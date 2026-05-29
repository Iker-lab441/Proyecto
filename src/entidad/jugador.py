import arcade

import util.io
import util.texturas as texturas
import config.controles as controles


class Jugador(arcade.Sprite):
    _VELOCIDAD: float = 400.0
    _HP: int = 3
    _FRAMES_PER_ANIM: int = 10

    def __init__(self, scale: float, center_x: float, center_y: float) -> None:
        super().__init__(None, scale, center_x, center_y)

        self.texturas_idle: list[arcade.Texture] = texturas.Jugador.IDLE
        self.texturas_correr: list[arcade.Texture] = texturas.Jugador.RUN
        self.texturas_saltar: list[arcade.Texture] = texturas.Jugador.JUMP
        self.texturas_caer: list[arcade.Texture] = texturas.Jugador.FALL

        self._en_suelo: bool = True

        self._hp: int = self._HP
        self._muerto: bool = False

    def update(self, delta_time: float) -> None:
        super().update(delta_time)

        if self.change_x != 0:
            self.scale_x = util.signo(self.change_x) * abs(self.scale_x)

        self.cur_texture_index += 1
        self.textures = self.texturas_idle

        change_x_anterior = self.change_x

        self._andar(delta_time)
        self._saltar(delta_time)

        if change_x_anterior != 0 and self.change_x == 0:
            self.cur_texture_index = 0

        self.cur_texture_index %= len(self.textures) * self._FRAMES_PER_ANIM
        self.texture = self.textures[self.cur_texture_index // self._FRAMES_PER_ANIM]

    def _andar(self, delta_time: float) -> None:
        change_x_anterior: float = self.change_x
        self.change_x = 0

        if util.io.tecla_mantenida(controles.jugador_izquierda):
            self.change_x -= self._VELOCIDAD * delta_time

        if util.io.tecla_mantenida(controles.jugador_derecha):
            self.change_x += self._VELOCIDAD * delta_time

        # No debería hacer la animación de correr si está quieto
        if self.change_x == 0:
            return

        # Las animaciones de salto tienen prioridad ante las de correr
        if not self._en_suelo:
            return

        if util.signo(change_x_anterior) != util.signo(self.change_x):
            self.cur_texture_index = 0
        else:
            self.cur_texture_index += 1

        if self.change_x != 0:
            self.textures = self.texturas_correr

    def _saltar(self, delta_time: float) -> None:
        if util.io.tecla_justo_pulsada(controles.jugador_salto):
            self.change_y = 10
            self._en_suelo = False

        if self.change_y > 0:
            self.change_y -= delta_time * 10
            self.cur_texture_index += 1
            self.textures = self.texturas_saltar
        elif not self._en_suelo:
            self.cur_texture_index += 1
            self.textures = self.texturas_caer

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
import arcade

import util.io
import util.texturas as texturas
import config.controles as controles


class Jugador(arcade.Sprite):
    _VELOCIDAD: float = 300.0
    _MAX_SALTO_MURO: int = 1
    _HP: int = 3
    _FRAMES_PER_ANIM: int = 10

    def __init__(self, scale: float, center_x: float, center_y: float, distancia_al_suelo: float, muros: arcade.SpriteList[arcade.Sprite]) -> None:
        super().__init__(None, scale, center_x, center_y)

        self._distancia_al_suelo: float = distancia_al_suelo
        self._muros: arcade.SpriteList[arcade.Sprite] = muros
        self._contador_salto_muro: int = 0

        self._texturas_idle: list[arcade.Texture] = texturas.Jugador.IDLE
        self._texturas_correr: list[arcade.Texture] = texturas.Jugador.RUN
        self._texturas_saltar: list[arcade.Texture] = texturas.Jugador.JUMP
        self._texturas_caer: list[arcade.Texture] = texturas.Jugador.FALL

        self._en_suelo: bool = True
        self._en_muro: bool = False

        self._velocidad = self._VELOCIDAD
        self._hp: int = self._HP
        self._muerto: bool = False

    def update(self, delta_time: float) -> None:
        super().update(delta_time)

        self.center_y -= self._distancia_al_suelo
        self._en_suelo = bool(self.collides_with_list(self._muros))
        self.center_y += self._distancia_al_suelo

        if self._en_suelo:
            self._en_muro = False
            self._contador_salto_muro = 0
        else:
            self.center_x += self._velocidad * delta_time
            self._en_muro = bool(self.collides_with_list(self._muros))
            self.center_x -= self._velocidad * delta_time
            if not self._en_muro:
                self.center_x -= self._velocidad * delta_time
                self._en_muro = bool(self.collides_with_list(self._muros))
                self.center_x += self._velocidad * delta_time

        self._velocidad = self._VELOCIDAD if self._en_suelo else self._VELOCIDAD * 0.8

        if self.change_x != 0:
            self.scale_x = util.signo(self.change_x) * abs(self.scale_x)

        self.cur_texture_index += 1
        self.textures = self._texturas_idle

        change_x_anterior = self.change_x

        self._andar(delta_time)
        self._saltar(delta_time)

        if change_x_anterior != 0 and self.change_x == 0:
            self.cur_texture_index = 0

        self.cur_texture_index %= len(self.textures) * self._FRAMES_PER_ANIM
        self.texture = self.textures[self.cur_texture_index // self._FRAMES_PER_ANIM]

        print(self._en_muro)

    def _andar(self, delta_time: float) -> None:
        change_x_anterior: float = self.change_x
        self.change_x = 0

        if util.io.tecla_mantenida(controles.jugador_izquierda):
            self.change_x -= self._velocidad * delta_time

        if util.io.tecla_mantenida(controles.jugador_derecha):
            self.change_x += self._velocidad * delta_time

        change_x = self.change_x
        self.center_x += change_x
        if self.collides_with_list(self._muros):
            self.change_x = 0
        self.center_x -= change_x

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
            self.textures = self._texturas_correr

    def _saltar(self, delta_time: float) -> None:
        if util.io.tecla_justo_pulsada(controles.jugador_salto):
            if self._en_suelo or self._en_muro and self._contador_salto_muro < self._MAX_SALTO_MURO:
                self.change_y = 10
                if self._en_muro:
                    self._contador_salto_muro += 1

        if self.change_y > 0:
            self.change_y -= delta_time * 10
            self.cur_texture_index += 1
            self.textures = self._texturas_saltar
        elif not self._en_suelo:
            self.cur_texture_index += 1
            self.textures = self._texturas_caer

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
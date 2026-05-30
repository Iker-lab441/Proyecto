import random

import arcade

import util
from util import texturas
from entidad.jugador import Jugador

class EnemigoPerseguidor(arcade.Sprite):
    _MIN_TIEMPO_IDLE: float = 1.0
    _MAX_TIEMPO_IDLE: float = 3.0
    _MIN_DISTANCIA_AGGRO: float = 300.0
    _MAX_DISTANCIA_AGGRO: float = 600.0
    _VELOCIDAD: float = 300.0
    _FRAMES_PER_ANIM: int = 10

    def __init__(self, jugador: Jugador, muros: arcade.SpriteList[arcade.Sprite], distancia_al_suelo: float, scale: float = 1, center_x: float = 0, center_y: float = 0, angle: float = 0) -> None:
        super().__init__(None, scale, center_x, center_y, angle)

        self.jugador: Jugador = jugador
        self.jugador_visto: bool = False

        self.muros: arcade.SpriteList[arcade.Sprite] = muros
        self.distancia_al_suelo: float = distancia_al_suelo

        self.contador_idle: float = 0
        self.dir: int = 1

        self._en_suelo: bool = True

    def update(self, delta_time: float) -> None:
        self.comprobar_suelo()

        distancia = arcade.math.get_distance(self.center_x, 0, self.jugador.center_x, 0)

        jugador_visto_anterior = self.jugador_visto
        self.jugador_visto = distancia <= self._MAX_DISTANCIA_AGGRO if jugador_visto_anterior else distancia <= self._MIN_DISTANCIA_AGGRO

        if not self.jugador_visto and jugador_visto_anterior:
            self._cambiar_direccion()
            self.contador_idle = self._MAX_TIEMPO_IDLE
            self.dir = random.choice((-1, 1))

        if self.jugador_visto:
            self.contador_idle = 0

            if distancia <= self._VELOCIDAD * delta_time:
                self.center_x = self.jugador.center_x
            else:
                self._perseguir_jugador(delta_time)
        elif self.contador_idle > 0:
            self.contador_idle -= delta_time

            if self.contador_idle <= 0:
                self.change_x = self._VELOCIDAD * self.dir * delta_time
        else:
            self._merodear()

    def comprobar_suelo(self) -> None:
        self.center_y += min(-self.distancia_al_suelo, self.change_y)
        self._en_suelo = bool(self.collides_with_list(self.muros))
        self.center_y -= min(-self.distancia_al_suelo, self.change_y)

    def _perseguir_jugador(self, delta_time: float) -> None:
        self.contador_idle = 0
        self.dir = util.signo(self.jugador.center_x - self.center_x)
        self.change_x = self._VELOCIDAD * self.dir * delta_time

    def _merodear(self) -> None:
        change_x_anterior = self.change_x
        self.center_x += change_x_anterior

        if self.collides_with_list(self.muros):
            print("HERE")
            # Si choca contra una pared, cambia de dirección
            self._cambiar_direccion()
        else:
            self.center_y -= self.distancia_al_suelo

            if not self.collides_with_list(self.muros):
                # Si seguir andando hace que se caiga de una plataforma, cambia de dirección
                self._cambiar_direccion()

            self.center_y += self.distancia_al_suelo

        self.center_x -= change_x_anterior

    def _cambiar_direccion(self) -> None:
        self.contador_idle = random.uniform(self._MIN_TIEMPO_IDLE, self._MAX_TIEMPO_IDLE)
        self.dir = -self.dir
        self.change_x = 0

    def update_animation(self, delta_time: float) -> None:
        self.cur_texture_index += 1

        if self.change_x == 0:
            self._cambiar_anim(texturas.Npcs.GOBLIN_IDLE)
        else:
            scale_x_anterior = self.scale_x
            self.scale_x = abs(scale_x_anterior) * util.signo(self.change_x)

            if self.scale_x != scale_x_anterior:
                self.cur_texture_index = 0

            self._cambiar_anim(texturas.Npcs.GOBLIN_RUN)

        self.cur_texture_index %= len(self.textures) * self._FRAMES_PER_ANIM
        self.texture = self.textures[self.cur_texture_index // self._FRAMES_PER_ANIM]

    def _cambiar_anim(self, anim: list[arcade.Texture]) -> None:
        if self.textures is not anim:
            self.cur_texture_index = 0
            self.textures = anim

    def on_collide(self, entidad: arcade.Sprite) -> None:
        if isinstance(entidad, Jugador):
            entidad.dañar()

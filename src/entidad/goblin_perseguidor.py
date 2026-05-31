import random

import arcade

from entidad.mob import Mob
import util
from util import texturas
from util import globales
from entidad.jugador import Jugador

class GoblinPerseguidor(Mob):
    _MIN_TIEMPO_IDLE: float = 1.0
    _MAX_TIEMPO_IDLE: float = 3.0
    _MIN_DISTANCIA_AGGRO: float = 300.0
    _MAX_DISTANCIA_AGGRO: float = 600.0

    def __init__(self, scale: float = 1, center_x: float = 0, center_y: float = 0) -> None:
        super().__init__(hp=3, velocidad_base=300, frames_por_textura=10, texture=texturas.Npcs.GOBLIN_IDLE[0], scale=scale, center_x=center_x, center_y=center_y)
        self.jugador_visto: bool = False

        self.contador_idle: float = 0.1
        self.dir: int = 1

        self._en_suelo: bool = True

    def update(self, delta_time: float) -> None:
        super().update(delta_time)

        distancia = arcade.get_distance_between_sprites(self, globales.jugador)

        jugador_visto_anterior = self.jugador_visto
        self.jugador_visto = distancia <= self._MAX_DISTANCIA_AGGRO if jugador_visto_anterior else distancia <= self._MIN_DISTANCIA_AGGRO

        if not self.jugador_visto and jugador_visto_anterior:
            self._cambiar_direccion()
            self.contador_idle = self._MAX_TIEMPO_IDLE
            self.dir = random.choice((-1, 1))

        if self.jugador_visto:
            self.contador_idle = 0

            if distancia <= self._velocidad_base * delta_time:
                self.center_x = globales.jugador.center_x
            else:
                self._perseguir_jugador(delta_time)
        elif self.contador_idle > 0:
            self.contador_idle -= delta_time

            if self.contador_idle <= 0:
                self.change_x = self._velocidad_base * random.uniform(0.5, 1) * self.dir * delta_time
        else:
            self._merodear()

    def _perseguir_jugador(self, delta_time: float) -> None:
        self.contador_idle = 0
        self.dir = util.signo(globales.jugador.center_x - self.center_x)
        self.change_x = self._velocidad_base * self.dir * delta_time

    def _merodear(self) -> None:
        change_x_anterior = self.change_x
        self.center_x += change_x_anterior

        if self.collides_with_list(globales.paredes):
            # Si choca contra una pared, cambia de dirección
            self._cambiar_direccion()
        else:
            self.center_y -= self._distancia_al_suelo

            if not self.collides_with_list(globales.suelos):
                # Si seguir andando hace que se caiga de una plataforma, cambia de dirección
                self._cambiar_direccion()

            self.center_y += self._distancia_al_suelo

        self.center_x -= change_x_anterior

    def _cambiar_direccion(self) -> None:
        self.contador_idle = random.uniform(self._MIN_TIEMPO_IDLE, self._MAX_TIEMPO_IDLE)
        self.dir = -self.dir
        self.change_x = 0

    def update_animation(self, delta_time: float) -> None:
        self._avanzar_animacion()

        if self.change_x == 0:
            self._cambiar_animacion(texturas.Npcs.GOBLIN_IDLE)
        else:
            scale_x_anterior = self.scale_x
            self.scale_x = abs(scale_x_anterior) * util.signo(self.change_x)

            if self.scale_x != scale_x_anterior:
                self.cur_texture_index = 0

            self._cambiar_animacion(texturas.Npcs.GOBLIN_RUN)

        self._mostrar_animacion()

    def on_collide(self, entidad: arcade.Sprite) -> None:
        if isinstance(entidad, Jugador):
            entidad.dañar()

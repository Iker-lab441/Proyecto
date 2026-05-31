import random

import arcade

from entidad.mob import Mob
from entidad.bola_de_fuego import BolaDeFuego
import util
from util import texturas
from util import globales
from entidad.jugador import Jugador

class GoblinDisparador(Mob):
    _MIN_TIEMPO_IDLE: float = 1.0
    _MAX_TIEMPO_IDLE: float = 3.0
    _MIN_DISTANCIA_AGGRO: float = 600.0
    _MAX_DISTANCIA_AGGRO: float = 1200.0
    _TIEMPO_DISPARO: float = 3.0

    def __init__(self, scale: float = 1, center_x: float = 0, center_y: float = 0) -> None:
        super().__init__(hp=3, velocidad_base=300, frames_por_textura=10, texture=texturas.Npcs.GOBLIN_IDLE[0], scale=scale, center_x=center_x, center_y=center_y)

        self._jugador_visto: bool = False
        self._muriendo: bool = False

        self._contador_disparo: float = 0
        self._dir: int = 1

    def update(self, delta_time: float) -> None:
        if self._muriendo:
            self.change_x = 0
            return

        super().update(delta_time)

        distancia = arcade.get_distance_between_sprites(self, globales.jugador)

        jugador_visto_anterior = self._jugador_visto
        self._jugador_visto = distancia <= self._MAX_DISTANCIA_AGGRO if jugador_visto_anterior else distancia <= self._MIN_DISTANCIA_AGGRO

        if not self._jugador_visto:
            return

        if self._jugador_visto and not jugador_visto_anterior:
            globales.audio.reproducir("goblin", volumen=2)
            self._contador_disparo = 0

        self._contador_disparo -= delta_time

        if self._contador_disparo > 0:
            return

        self._contador_disparo = self._TIEMPO_DISPARO

        velocidad = (arcade.Vec2(*globales.jugador.position) - self.position).normalize() * self._velocidad_base * delta_time
        globales.nivel.add_proyectil(BolaDeFuego(velocidad.x, velocidad.y, self))

    def update_animation(self, delta_time: float) -> None:
        self._avanzar_animacion()

        if self._muriendo:
            self._cambiar_animacion(texturas.Npcs.GOBLIN_DEFEATED)
            if self.cur_texture_index // self._frames_por_textura >= len(self.textures):
                arcade.Sprite.kill(self)
        elif self._jugador_visto:
            self._cambiar_animacion(texturas.Npcs.GOBLIN_RUN)
            scale_x = abs(self.scale_x) * util.signo(globales.jugador.center_x - self.center_x)
            if scale_x != 0:
                self.scale_x = scale_x
        else:
            self._cambiar_animacion(texturas.Npcs.GOBLIN_IDLE)

        self._mostrar_animacion()

    def on_collide(self, entidad: arcade.Sprite) -> None:
        if not self._muriendo and isinstance(entidad, Jugador):
            entidad.dañar()

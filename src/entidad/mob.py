from abc import ABC, abstractmethod

import arcade

import util
from util import globales

class Mob(arcade.Sprite, ABC):
    @abstractmethod
    def __init__(self, hp: int, velocidad_base: float, frames_por_textura: int,
                 texture: arcade.Texture, scale: float, center_x: float, center_y: float) -> None:
        super().__init__(texture, scale, center_x, center_y)

        self._distancia_al_suelo: float = 6
        self._frames_por_textura: int = frames_por_textura

        self._en_suelo: bool = True
        self._en_pared: bool = False
        self._velocidad_base: float = velocidad_base

        self._hp: int = hp
        self._muerto: bool = False

    def update(self, delta_time: float) -> None:
        self.center_y -= self._distancia_al_suelo
        self._en_suelo = bool(self.collides_with_list(globales.suelos))
        self.center_y += self._distancia_al_suelo

        incremento_x = util.signo(self.scale_x) * self._velocidad_base * delta_time

        self.center_x += incremento_x
        self._en_pared = bool(self.collides_with_list(globales.paredes))
        self.center_x -= incremento_x

    def _a_punto_de_chocarse_con_pared(self) -> bool:
        self.center_x += self.change_x
        salida = bool(self.collides_with_list(globales.paredes))
        self.center_x -= self.change_x

        return salida

    def _avanzar_animacion(self) -> None:
        self.cur_texture_index += 1

    def _mostrar_animacion(self) -> None:
        self.cur_texture_index %= len(self.textures) * self._frames_por_textura
        self.texture = self.textures[self.cur_texture_index // self._frames_por_textura]

    def _cambiar_animacion(self, anim: list[arcade.Texture]) -> None:
        if self.textures is not anim:
            self.cur_texture_index = 0
            self.textures = anim

    def dañar(self) -> None:
        self._hp -= 1
        if self._hp <= 0:
            self._muerto = True

    @property
    def esta_muerto(self) -> bool:
        return self._muerto

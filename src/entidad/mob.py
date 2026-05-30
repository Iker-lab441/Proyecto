from abc import ABC

import arcade

import util
import util.obstaculos

class Mob(arcade.Sprite, ABC):
    def __init__(self, hp: int, velocidad_base: float,
                 texture: arcade.Texture, scale: float, center_x: float, center_y: float) -> None:
        super().__init__(texture, scale, center_x, center_y)

        self._distancia_al_suelo: float = 6
        print("DIST: ", self._distancia_al_suelo)

        self._en_suelo: bool = True
        self._en_pared: bool = False
        self._velocidad_base: float = velocidad_base

        self._hp: int = hp
        self._muerto: bool = False

    def update(self, delta_time: float) -> None:
        self.center_y -= self._distancia_al_suelo
        self._en_suelo = bool(self.collides_with_list(util.obstaculos.suelos))
        self.center_y += self._distancia_al_suelo

        incremento_x = util.signo(self.scale_x) * self._velocidad_base * delta_time

        self.center_x += incremento_x
        self._en_pared = bool(self.collides_with_list(util.obstaculos.paredes))
        self.center_x -= incremento_x

    def a_punto_de_chocarse_con_pared(self) -> bool:
        self.center_x += self.change_x
        salida = bool(self.collides_with_list(util.obstaculos.paredes))
        self.center_x -= self.change_x

        return salida

    def dañar(self) -> None:
        self._hp -= 1
        if self._hp <= 0:
            self._muerto = True

    @property
    def esta_muerto(self) -> bool:
        return self._muerto

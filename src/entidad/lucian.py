from abc import ABC, abstractmethod
import random

import arcade
from arcade import Vec2

from entidad.mob import Mob
import util
from util import texturas, globales


class LucianState(ABC):
    def __init__(self, lucian: "Lucian") -> None:
        self.lucian: Lucian = lucian

    @abstractmethod
    def update(self, delta_time: float) -> None:
        pass

    @abstractmethod
    def update_animation(self, delta_time: float) -> None:
        pass


class LucianStateIdle(LucianState):
    def __init__(self, lucian: "Lucian") -> None:
        super().__init__(lucian)
        self.contador: float = 1

    def update(self, delta_time: float) -> None:
        self.contador -= delta_time

        if self.contador <= 0:
            self.lucian.state = LucianStateEmbestida(self.lucian)

    def update_animation(self, delta_time: float) -> None:
        pass


class LucianStateEmbestida(LucianState):
    def __init__(self, lucian: "Lucian") -> None:
        super().__init__(lucian)

        inicio, fin = random.choice(list(self.lucian.embestidas.items()))
        self.lucian.position = inicio

        self.fin: Vec2 = Vec2(*fin)
        self.dir: Vec2 = (self.fin - self.lucian.position).normalize()

        self.lucian._cambiar_animacion(texturas.Npcs.LUCIAN_RUN)
        self.lucian.scale_x = abs(self.lucian.scale_x) * util.signo(self.dir.x)

    def update(self, delta_time: float) -> None:
        self.lucian.velocity = self.lucian.velocidad_base * self.dir * delta_time

        distancia_actual = arcade.math.get_distance(self.lucian.center_x, self.lucian.center_y, self.fin.x, self.fin.y)
        distancia_siguiente = arcade.math.get_distance(self.lucian.center_x + self.lucian.change_x, self.lucian.center_y + self.lucian.change_y, self.fin.x, self.fin.y)

        if distancia_siguiente > distancia_actual:
            self.lucian.state = LucianStateIdle(self.lucian)

        arcade.Sprite.update(self.lucian, delta_time)

    def update_animation(self, delta_time: float) -> None:
        pass


class Lucian(Mob):
    def __init__(self, embestidas: dict[tuple[float, float], tuple[float, float]], scale: float, center_x: float, center_y: float) -> None:
        super().__init__(hp=30, velocidad_base=1000, frames_por_textura=10, texture=texturas.Npcs.LUCIAN_IDLE[0], scale=scale, center_x=center_x, center_y=center_y)
        self.textures = texturas.Npcs.LUCIAN_IDLE

        self.embestidas: dict[tuple[float, float], tuple[float, float]] = embestidas
        self.state: LucianState = LucianStateIdle(self)

    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        self.state.update(delta_time)

    def update_animation(self, delta_time: float) -> None:
        self._avanzar_animacion()
        self.state.update_animation(delta_time)
        self._mostrar_animacion()

    @property
    def velocidad_base(self) -> float:
        return self._velocidad_base

from abc import ABC, abstractmethod
from collections import deque
import random

import arcade
from arcade import Vec2

from entidad.mob import Mob
from entidad.proyectil import Proyectil
import util
from util import texturas, globales


class LucianState(ABC):
    def __init__(self, lucian: "Lucian") -> None:
        self.lucian: Lucian = lucian
        lucian.velocity = 0, 0

    @abstractmethod
    def update(self, delta_time: float) -> None:
        pass

    def update_animation(self, delta_time: float) -> None:
        pass


class LucianStateIdle(LucianState):
    def __init__(self, lucian: "Lucian") -> None:
        super().__init__(lucian)
        self.contador: float = 2

    def update(self, delta_time: float) -> None:
        self.contador -= delta_time

        if self.contador <= 0:
            self.lucian.state = self.lucian.next_ataque()


class LucianStateEmbestida(LucianState):
    def __init__(self, lucian: "Lucian") -> None:
        super().__init__(lucian)

        inicio, fin = random.choice(list(self.lucian.embestidas.items()))

        if random.randint(0, 1) == 0:
            inicio, fin = fin, inicio

        self.lucian.position = inicio
        self.fin: Vec2 = Vec2(*fin)
        self.dir: Vec2 = (self.fin - self.lucian.position).normalize()

        self.lucian._cambiar_animacion(texturas.Npcs.LUCIAN_RUN)
        self.lucian.scale_x = abs(self.lucian.scale_x) * util.signo(self.dir.x)

        self.contador_parado: float = 0.5

    def update(self, delta_time: float) -> None:
        self.contador_parado -= delta_time

        if self.contador_parado > 0:
            return

        self.lucian.velocity = self.lucian.velocidad_base * self.dir * delta_time

        distancia_actual = arcade.math.get_distance(self.lucian.center_x, self.lucian.center_y, self.fin.x, self.fin.y)
        distancia_siguiente = arcade.math.get_distance(self.lucian.center_x + self.lucian.change_x, self.lucian.center_y + self.lucian.change_y, self.fin.x, self.fin.y)

        if distancia_siguiente > distancia_actual:
            self.lucian.esconder()
            self.lucian.state = LucianStateIdle(self.lucian)

        arcade.Sprite.update(self.lucian, delta_time)

    def update_animation(self, delta_time: float) -> None:
        r, g, b, _ = self.lucian.color

        if self.contador_parado > 0:
            self.lucian.color = (r, g, b, 128)
        else:
            self.lucian.color = (r, g, b, 255)


class LucianStateDisparo(LucianState):
    CONTADOR_MAX: float = 8
    CONTADOR_DISPARO_MAX: float = 2

    def __init__(self, lucian: "Lucian") -> None:
        super().__init__(lucian)
        self.lucian.esconder()

        self.contador: float = self.CONTADOR_MAX
        self.contador_disparo: float = self.CONTADOR_DISPARO_MAX

    def update(self, delta_time: float) -> None:
        self.contador -= delta_time
        self.contador_disparo -= delta_time

        if self.contador_disparo <= self.CONTADOR_DISPARO_MAX / 2:
            self.lucian.esconder()

        if self.contador_disparo > 0:
            return

        self.contador_disparo = self.CONTADOR_DISPARO_MAX

        pos_disparo = random.choice(self.lucian.posiciones_disparo)
        self.lucian.position = pos_disparo

        progreso_contador = 1 - self.contador / self.CONTADOR_MAX
        velocidad = (globales.jugador.position - pos_disparo).normalize() * self.lucian.velocidad_base * delta_time * progreso_contador

        globales.nivel.add_proyectil(Proyectil(texturas.Npcs.LUCIAN_IDLE[0], velocidad.x, velocidad.y, 10, self.lucian))
        globales.nivel.add_proyectil(Proyectil(texturas.Npcs.LUCIAN_IDLE[0], velocidad.x * 0.9, velocidad.y * 1.1, 10, self.lucian))
        globales.nivel.add_proyectil(Proyectil(texturas.Npcs.LUCIAN_IDLE[0], velocidad.x * 1.1, velocidad.y * 0.9, 10, self.lucian))

        if self.contador <= 0:
            self.lucian.state = LucianStateIdle(self.lucian)

    def update_animation(self, delta_time: float) -> None:
        self.lucian._cambiar_animacion(texturas.Npcs.LUCIAN_JUMP_LOOP)
        self.lucian.scale_x = abs(self.lucian.scale_x) * util.signo(globales.jugador.center_x - self.lucian.center_x)


class Lucian(Mob):
    def __init__(self, embestidas: dict[tuple[float, float], tuple[float, float]], posiciones_disparo: list[Vec2], scale: float, center_x: float, center_y: float) -> None:
        super().__init__(hp=30, velocidad_base=1000, frames_por_textura=10, texture=texturas.Npcs.LUCIAN_IDLE[0], scale=scale, center_x=center_x, center_y=center_y)

        self.embestidas: dict[tuple[float, float], tuple[float, float]] = embestidas
        self.posiciones_disparo: list[Vec2] = posiciones_disparo

        self.textures = texturas.Npcs.LUCIAN_IDLE
        self.state: LucianState = LucianStateIdle(self)

        self._ataques: list[type] = [LucianStateEmbestida, LucianStateEmbestida, LucianStateDisparo, LucianStateEmbestida, LucianStateDisparo, LucianStateDisparo]
        self._indice_ataque: int = 0

    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        self.state.update(delta_time)

    def update_animation(self, delta_time: float) -> None:
        self._avanzar_animacion()
        self.state.update_animation(delta_time)
        self._mostrar_animacion()

    def next_ataque(self) -> LucianState:
        self._indice_ataque = (self._indice_ataque + 1) % len(self._ataques)
        return self._ataques[self._indice_ataque - 1](self)

    def esconder(self) -> None:
        self.position = (-256, -256)

    @property
    def velocidad_base(self) -> float:
        return self._velocidad_base

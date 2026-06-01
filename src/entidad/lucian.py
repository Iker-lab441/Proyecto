from abc import ABC, abstractmethod
from collections import deque
import random

import arcade
from arcade import Vec2

from entidad.mob import Mob
from entidad.proyectil import Proyectil
from entidad.entidad import Entidad
from entidad.jugador import Jugador
import util
from util import texturas, globales


class LucianState(ABC):
    def __init__(self, lucian: "Lucian") -> None:
        self.lucian: Lucian = lucian
        lucian.tiene_fisicas = False
        lucian.velocity = 0, 0
        lucian.tangible = True

    @abstractmethod
    def update(self, delta_time: float) -> None:
        pass

    def update_animation(self, delta_time: float) -> None:
        scale_x = abs(self.lucian.scale_x) * util.signo(globales.jugador.center_x - self.lucian.center_x)

        if scale_x != 0:
            self.lucian.scale_x = scale_x


class LucianStateIdle(LucianState):
    def __init__(self, lucian) -> None:
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

        lucian.position = inicio
        self.fin: Vec2 = Vec2(*fin)
        self.dir: Vec2 = (self.fin - self.lucian.position).normalize()

        self.lucian._cambiar_animacion(texturas.Npcs.LUCIAN_RUN)
        self.lucian.scale_x = abs(self.lucian.scale_x) * util.signo(self.dir.x)

        self.contador_parado: float = 0.5
        globales.audio.reproducir("ataque_lucian", volumen=0.7)

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
        self.lucian.tangible = self.contador_parado <= 0


class LucianStateDisparo(LucianState):
    CONTADOR_MAX: float = 8
    CONTADOR_DISPARO_MAX: float = 2

    def __init__(self, lucian: "Lucian") -> None:
        super().__init__(lucian)
        lucian.esconder()

        self.contador: float = self.CONTADOR_MAX - self.CONTADOR_DISPARO_MAX
        self.contador_disparo: float = 0

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

        globales.audio.reproducir("disparo_lucian", volumen=0.6)
        globales.nivel.add_proyectil(Proyectil(texturas.Proyectiles.BOLA_FUEGO_OSCURA[0], velocidad.x, velocidad.y, 10, self.lucian))
        globales.nivel.add_proyectil(Proyectil(texturas.Proyectiles.BOLA_FUEGO_OSCURA[0], velocidad.x * 0.9, velocidad.y * 1.1, 10, self.lucian))
        globales.nivel.add_proyectil(Proyectil(texturas.Proyectiles.BOLA_FUEGO_OSCURA[0], velocidad.x * 1.1, velocidad.y * 0.9, 10, self.lucian))

        if self.contador <= 0:
            self.lucian.state = LucianStateIdle(self.lucian)

    def update_animation(self, delta_time: float) -> None:
        super().update_animation(delta_time)
        self.lucian.cambiar_animacion(texturas.Npcs.LUCIAN_JUMP_LOOP)


class LucianStateCaida(LucianState):
    def __init__(self, lucian: "Lucian") -> None:
        super().__init__(lucian)

        lucian.tiene_fisicas = True
        lucian.cambiar_animacion(texturas.Npcs.LUCIAN_JUMP_LOOP)

        lucian.center_y = lucian.caida_y
        lucian.center_x = globales.jugador.center_x

    def update(self, delta_time: float) -> None:
        pass

    def update_animation(self, delta_time: float) -> None:
        super().update_animation(delta_time)

        print(self.lucian.en_suelo)
        if self.lucian.change_y != 0:
            self.lucian.cambiar_animacion(texturas.Npcs.LUCIAN_JUMP_LOOP)
        elif self.lucian.textures is texturas.Npcs.LUCIAN_JUMP_LOOP:
            self.lucian.cambiar_animacion(texturas.Npcs.LUCIAN_FALL[1:])
        elif self.lucian.cur_texture_index // self.lucian.frames_por_textura >= len(self.lucian.textures):
            self.lucian.cambiar_animacion(texturas.Npcs.LUCIAN_IDLE)
            self.lucian.state = LucianStateIdle(self.lucian)
            self.lucian.state.contador -= 1.5


class LucianStateMuriendo(LucianState):
    def update(self, delta_time: float) -> None:
        pass

    def update_animation(self, delta_time: float) -> None:
        self.lucian.cambiar_animacion(texturas.Npcs.LUCIAN_DEFEATED)
        if self.lucian.cur_texture_index // self.lucian.frames_por_textura >= len(self.lucian.textures):
            arcade.Sprite.kill(self.lucian)
            from menu.escena_final import EscenaFinal
            self.lucian.window.show_view(EscenaFinal())


class Lucian(Mob):
    def __init__(self, embestidas: dict[tuple[float, float], tuple[float, float]], posiciones_disparo: list[Vec2], caida_x: float, caida_y: float, distancia_lateral_caida: float,
                 scale: float, center_x: float, center_y: float) -> None:
        super().__init__(hp=30, velocidad_base=1000, frames_por_textura=10, texture=texturas.Npcs.LUCIAN_IDLE[0], scale=scale, center_x=center_x, center_y=center_y)

        self.embestidas: dict[tuple[float, float], tuple[float, float]] = embestidas
        self.posiciones_disparo: list[Vec2] = posiciones_disparo

        self.caida_x: float = caida_x
        self.caida_y: float = caida_y
        self.distancia_lateral_caida: float = distancia_lateral_caida


        self.state: LucianState = LucianStateIdle(self)
        self._tangible: bool = False

        self.tiene_fisicas: bool = False
        self.textures = texturas.Npcs.LUCIAN_IDLE

        self._ataques: list[type] = [LucianStateEmbestida, LucianStateEmbestida, LucianStateDisparo, LucianStateEmbestida, LucianStateCaida, LucianStateCaida, LucianStateDisparo, LucianStateCaida, LucianStateCaida, LucianStateCaida, LucianStateCaida, LucianStateDisparo]
        self._indice_ataque: int = 0

    def update(self, delta_time: float) -> None:
        if self._muriendo:
            self.state = LucianStateMuriendo(self)
            self._tangible = False

        # Ignora las plataformas coladizas
        suelos = globales.suelos
        globales.suelos = globales.paredes

        super().update(delta_time)

        globales.suelos = suelos

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

    def cambiar_animacion(self, anim: list[arcade.Texture]) -> None:
        self._cambiar_animacion(anim)

    def on_collide(self, entidad: Entidad) -> None:
        if not self._muriendo and isinstance(entidad, Jugador):
            entidad.dañar(2)

    @property
    def velocidad_base(self) -> float:
        return self._velocidad_base

    @property
    def en_suelo(self) -> float:
        return self._en_suelo

    @property
    def frames_por_textura(self) -> float:
        return self._frames_por_textura

    @property
    def tangible(self) -> bool:
        return self._tangible

    @tangible.setter
    def tangible(self, tangible: bool) -> None:
        self._tangible = tangible

        r, g, b, _ = self.color
        self.color = (r, g, b, 255 if self.tangible else 128)

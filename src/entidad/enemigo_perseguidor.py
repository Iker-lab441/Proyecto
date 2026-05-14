import random

import arcade

from entidad.jugador import Jugador

class EnemigoPerseguidor(arcade.Sprite):
    MIN_TIEMPO_IDLE: float = 0.1
    MAX_TIEMPO_IDLE: float = 2.0

    def __init__(self, scale = 1, center_x = 0, center_y = 0, angle = 0, **kwargs) -> None:
        super().__init__(None, scale, center_x, center_y, angle, **kwargs)
        
        self.jugador_visto: bool = False

    def update(self, delta_time = 1 / 60, *args, **kwargs) -> None:
        if self.contador_idle >= 0:
            self.contador_idle -= delta_time
        else:
            super().update(delta_time, *args, **kwargs)

    def on_ver_jugador(self, jugador: Jugador) -> None:
        self.jugador_visto = True
        self.velocity.x = jugador.center_x - self.center_x

    def on_dejar_de_ver_jugador(self) -> None:
        self.jugador_visto = False

    def on_collision_borde_plataforma(self) -> None:
        if not self.jugador_visto:
            self.contador_idle = random.randint(self.MIN_TIEMPO_IDLE, self.MAX_TIEMPO_IDLE)
            self.velocity_x = -self.velocity_x

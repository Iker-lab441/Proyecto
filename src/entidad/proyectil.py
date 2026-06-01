from abc import ABC, abstractmethod
import arcade

from entidad.mob import Mob

class Proyectil(arcade.Sprite, ABC):
    """
    Clase base abstracta para los proyectiles.
    Hereda de arcade.Sprite (que actúa como la base de las entidades en este proyecto) 
    y de ABC para hacerla abstracta.
    """

    def __init__(self, textura_o_animacion, change_x: float, change_y: float, perforacion: int, shooter: arcade.Sprite, *args, **kwargs):
        if isinstance(textura_o_animacion, list):
            self.animacion = textura_o_animacion
            super().__init__(self.animacion[0], *args, **kwargs)
        else:
            self.animacion = None
            super().__init__(textura_o_animacion, *args, **kwargs)
            
        self.cur_texture_index = 0
        self.tiempo_animacion = 0.0
        
        self.change_x = change_x
        self.change_y = change_y
        self.perforacion = perforacion
        self.shooter = shooter
        self.center_x = shooter.center_x
        self.center_y = shooter.center_y
        self.angle = arcade.math.get_angle_degrees(shooter.center_x, shooter.center_y, shooter.center_x +change_x, shooter.center_y + change_y)
        self.entidades_golpeadas = set()

    def update_animation(self, delta_time: float = 1/60, *args, **kwargs):
        if self.animacion:
            self.tiempo_animacion += delta_time
            if self.tiempo_animacion >= 0.1: 
                self.tiempo_animacion = 0
                self.cur_texture_index += 1
                if self.cur_texture_index >= len(self.animacion):
                    self.cur_texture_index = 0
                self.texture = self.animacion[self.cur_texture_index]

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        """
        El movimiento se maneja actualizando la posición según change_x y change_y.
        """
        super().update(delta_time, *args, **kwargs)
        # Nota: si el super().update no mueve el sprite basado en delta_time, 
        # puedes añadir la lógica aquí:
        # self.center_x += self.change_x * delta_time
        # self.center_y += self.change_y * delta_time

    def on_collide(self, entidad: arcade.Sprite) -> None:
        """
        Lógica de colisión con otras entidades.
        Hace daño a los Mobs (entidades con método dañar) menos al que lo ha disparado.
        """
        # Ignorar a quien disparó el proyectil o a los demás del mismo tipo
        if type(entidad) == type(self.shooter):
            return

        # Ignorar si ya hemos golpeado a esta entidad en frames anteriores
        if entidad in self.entidades_golpeadas:
            return

        # Comprobamos si la entidad puede recibir daño (es un Mob/personaje)
        if isinstance(entidad, Mob):
            from entidad.lucian import Lucian

            if isinstance(entidad, Lucian) and not entidad.tangible:
                return

            entidad.dañar()

            self.entidades_golpeadas.add(entidad)
            self.perforacion -= 1

            # Si se queda sin perforación, el proyectil se destruye
            if self.perforacion <= 0:
                self.kill()

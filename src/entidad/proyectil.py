from abc import ABC, abstractmethod
import arcade

class Proyectil(arcade.Sprite, ABC):
    """
    Clase base abstracta para los proyectiles.
    Hereda de arcade.Sprite (que actúa como la base de las entidades en este proyecto) 
    y de ABC para hacerla abstracta.
    """
    
    def __init__(self, texture, change_x: float, change_y: float, perforacion: int, shooter: arcade.Sprite, *args, **kwargs):
        super().__init__(texture, *args, **kwargs)
        self.change_x = change_x
        self.change_y = change_y
        self.perforacion = perforacion
        self.shooter = shooter
        self.entidades_golpeadas = set()

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
        # Ignorar a quien disparó el proyectil
        if entidad == self.shooter:
            return
            
        # Ignorar si ya hemos golpeado a esta entidad en frames anteriores
        if entidad in self.entidades_golpeadas:
            return

        # Comprobamos si la entidad puede recibir daño (es un Mob/personaje)
        if hasattr(entidad, "dañar"):
            if callable(entidad.dañar):
                entidad.dañar()
            
            self.entidades_golpeadas.add(entidad)
            self.perforacion -= 1
            
            # Si se queda sin perforación, el proyectil se destruye
            if self.perforacion <= 0:
                self.kill()

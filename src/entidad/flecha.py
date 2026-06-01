import arcade
from entidad.proyectil import Proyectil
from util import texturas 

class Flecha(Proyectil):
    def __init__(self, change_x: float, change_y: float, shooter: arcade.Sprite):
        super().__init__(
            textures=texturas.Proyectiles.FLECHA,
            change_x=change_x,
            change_y=change_y,
            perforacion=1,
            shooter=shooter
        )

    def update(self, delta_time: float) -> None:
        # No llama a super().update porque lo actualiza el physics engine, ya que le afecta la gravedad
        self.angle = arcade.math.get_angle_degrees(self.center_x, self.center_y, self.center_x + self.change_x, self.center_y + self.change_y)

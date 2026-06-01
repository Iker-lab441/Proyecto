import arcade
from entidad.proyectil import Proyectil
from util import texturas 

class BolaDeFuego(Proyectil):
    def __init__(self, change_x: float, change_y: float, shooter: arcade.Sprite):
        super().__init__(
            texture=texturas.Proyectiles.BOLA_FUEGO[0],
            change_x=change_x,
            change_y=change_y,
            perforacion=3,
            shooter=shooter
        )

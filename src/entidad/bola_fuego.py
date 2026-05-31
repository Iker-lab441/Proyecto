import arcade
from entidad.proyectil import Proyectil 

class BolaDeFuego(Proyectil):
    def __init__(self, change_x: float, change_y: float, shooter: arcade.Sprite):
        textura = arcade.load_texture("bola_fuego.png")
        
        super().__init__(
            texture=textura,
            change_x=change_x,
            change_y=change_y,
            perforacion=3,
            shooter=shooter
        )
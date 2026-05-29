from tile.palanca import Palanca
from tile.puerta import Puerta


class PalancaPuerta(Palanca):
    def __init__(self, puerta: Puerta, center_x: float = 0, center_y: float = 0, angle: float = 0):
        super().__init__(puerta.abrir, puerta.cerrar, center_x, center_y, angle)
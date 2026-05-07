from tile.palanca import Palanca
from tile.puerta import Puerta


class PalancaPuerta(Palanca):
    def __init__(self, puerta: Puerta, center_x=0, center_y=0, angle=0, **kwargs):
        super().__init__(puerta.abrir, puerta.cerrar, center_x, center_y, angle, **kwargs)
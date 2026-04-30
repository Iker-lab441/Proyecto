# Clase Nivel
import arcade
from palanca import Palanca

TILE_SCALING = 1
class Nivel():
    def __init__(self):
        self.layer_options = {}
    def setup():
        self.layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
                "scaling": 2.5,
                "offset": (-128, 64),
                "custom_class": Palanca,
                "custom_class_args": {
                    "health": 100
                }
            }
        }
        tile_map = arcade.load_tilemap(
            f"assets\maps\\button_map.json",
            scaling=TILE_SCALING,
            layer_options=self.layer_options,
        )
        



#Pruebas---------------------#
def main():
    ventana = Ventana()
    nivel = Nivel()
    arcade.run()

if __name__ == "__main__":
    main()
#----------------------------#


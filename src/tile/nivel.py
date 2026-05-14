# Clase Nivel
import arcade
from pathlib import Path
import json
from  tile.palanca import Palanca
from entidad.jugador import Jugador
import util.nivel as niv

ROOT = Path(__file__).resolve().parent.parent.parent

"""class Prueba(arcade.Sprite): 
    def __init__(self, path_or_texture, scale):
        super().__init__(ROOT / "assets" / "images" / "ladrillo_musgoso.png", scale)"""

"""class Palanca(arcade.Sprite): 
    def __init__(self, path_or_texture, scale):
        super().__init__(ROOT / "assets" / "images" / "palanca2.png", scale)"""

TILE_SCALING = 1
class Nivel(arcade.View):
    def __init__(self, nivel: str | Path):
        super().__init__()
        self.scene = niv.crear_nivel(nivel)
    
    def on_draw(self):
        super().on_draw()
        self.scene.draw()


#Pruebas-------------------------------------#
def main():
    ventana = arcade.Window()
    nivel = Nivel("mapa_prueba_clase_nivel")
    ventana.show_view(nivel)
    arcade.run()

if __name__ == "__main__":
    main()
#--------------------------------------------#


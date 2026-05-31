# Clase Nivel
import arcade
from pathlib import Path
import json
from  tile.palanca import Palanca
from entidad.jugador import Jugador
import src.util.nivelito as niv
from util.camara import Camara

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
        resultado = niv.crear_nivel(nivel)
        self.scene = resultado[0]
        self.jugador = resultado[1]
        self.scene.add_sprite("Jugador", self.jugador)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.jugador,
            walls=self.scene["Muros"],
            gravity_constant=1,
        )
        ruta = ROOT / "assets" / "maps" / str(nivel+".json")
        self.tile_map = arcade.load_tilemap(
            ruta,
            scaling=TILE_SCALING,
        )
        self.camera = Camara()
        self.camera.zoom = 1
        self.camera.right_border = 8000 #self.tile_map.width*18*0.5
        self.camera.top_border = 6000 #self.tile_map.height*18*0.5

        
    
    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()
    
    def on_update(self, delta_time):
        self.jugador.update(delta_time)
        self.physics_engine.update()
        self.camera.position = self.jugador.position

        self.camera.on_update()

        #print(self.scene.get_sprite_list("Jugador")[0].__class__)


#Pruebas-------------------------------------#
def main():
    ventana = arcade.Window()
    nivel = Nivel("mapa_prueba_clase_nivel")
    ventana.show_view(nivel)
    arcade.run()

if __name__ == "__main__":
    main()
#--------------------------------------------#


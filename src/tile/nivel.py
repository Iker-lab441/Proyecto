# Clase Nivel
import arcade
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent.parent

class Prueba(arcade.Sprite): 
    def __init__(self, path_or_texture, scale):
        super().__init__(self, path_or_texture)
        

TILE_SCALING = 1
class Nivel(arcade.View):
    def __init__(self, nivel: str):
        super().__init__()
        self.nivel = json.load(open(ROOT / "assets" / "maps" / (nivel + ".json"), 'r', encoding='utf-8')) 
        self.layers = self._get_layers()
        self.layer_options = self._set_layer_options()
        self.tile_map = arcade.load_tilemap(
            ROOT / "assets" / "maps" / (nivel + ".json"),
            scaling=TILE_SCALING,
            layer_options=self.layer_options,
        )
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
    
    def _get_layers(self):
        list_layers = []
        for item in self.nivel["layers"]:
            list_layers.append(item["name"])
        return list_layers
    
    def _set_layer_options(self):
        layer_options = {}
        for layer in self.layers:
            if (layer == "Capa de patrones 1"): layer_options[layer] = {"use_spatial_hash": True, "custom_class": Prueba}
            else: layer_options[layer] = {"use_spatial_hash": True}
        return layer_options
    
    def on_draw(self):
        super().on_draw()
        self.scene.draw()


#Pruebas-------------------------------------#
def main():
    ventana = arcade.Window()
    nivel = Nivel("mapa_prueba_clase_nivel")
    ventana.show_view(nivel)
    nivel._get_layers()
    arcade.run()

if __name__ == "__main__":
    main()
#--------------------------------------------#


# Herramienta tratamiento del Tilemap
import arcade
from entidad.jugador import Jugador

def crear_nivel(nivel:str)-> arcade.Scene:



    with open((nivel + ".json"), 'r', encoding='utf-8') as archivo:
            dict_nivel = json.load(archivo)
            copy_dict = dict_nivel
            for layer in dict_nivel["layers"]:
                # Dibujar los bloques
                if layer["name"] == "Bloques":
                    dict_bloques = dict_nivel
                    dict_bloques["layers"] = layer["layers"]
                    scene = self._set_bloques(dict_bloques)
                if layer["name"] == "Entidades":
                    for entidad in layer["layers"]:
                        if entidad["name"] == "Jugador":
                            marcador = entidad["objects"][0]
                            jugador = Jugador(center_x=marcador["x"], center_y=marcador["y"], scale=2)
                            print(jugador.center_x)
                            print(marcador["name"])
                print(layer["name"])
                for layer in layer["layers"]:
                    print("    - " + layer["name"])
            #scene = self._set_bloques(dict_nivel)
            #print(self._get_layers(dict_nivel))
            scene.add_sprite("Jugador", jugador)
            print(scene.get_sprite_list("Jugador")[0].center_x)
        return scene
    
# Path = Path("assets") / "images" / "palanca1.png"
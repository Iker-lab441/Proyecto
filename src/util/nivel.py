# Herramienta tratamiento del Tilemap
from pathlib import Path
import json
import arcade
from entidad.jugador import Jugador

TILE_SCALING = 1

def _set_bloques(dict_bloques: dict, nivel:str) -> arcade.Scene:
    bloques = dict_bloques
    ruta = Path("assets") / "maps" / str("bloques.json")
    with open ("bloques.json", "w") as archivo:
        json.dump(bloques, archivo)
    ruta = Path("assets") / "maps" / str(nivel+".json")
    tile_map = arcade.load_tilemap(
        ruta,
        scaling=TILE_SCALING,
        layer_options= _set_layer_options(bloques),
    ) 
    scene = arcade.Scene.from_tilemap(tile_map)
    return scene

def _set_layer_options(bloques:dict):
        layer_options = {}
        for layer in bloques["layers"]:
            if(layer["name"] == "Muros"):
                layer_options[layer["name"]] = {"use_spatial_hash": True}
        return layer_options

def crear_nivel(nivel:str)-> arcade.Scene:
    ruta = Path("assets") / "maps" / str(nivel+".json")
    with open(ruta, 'r', encoding='utf-8') as archivo:
        dict_nivel = json.load(archivo)
        for layer in dict_nivel["layers"]:
            # Dibujar los bloques
            if layer["name"] == "Bloques":
                dict_bloques = dict_nivel
                dict_bloques["layers"] = layer["layers"]
                scene = _set_bloques(dict_bloques, nivel)
            if layer["name"] == "Entidades":
                for entidad in layer["layers"]:
                    if entidad["name"] == "Jugador":
                        marcador = entidad["objects"][0]
                        jugador = Jugador(center_x=marcador["x"], center_y=marcador["y"])
                        #jugador = Jugador(center_x=30, center_y=30)
                        print(jugador)
                        print(marcador["name"])
            print(layer["name"])
            for layer in layer["layers"]:
                print("    - " + layer["name"])
        #scene.add_sprite("Jugador", jugador)
        #print(scene.get_sprite_list("Jugador")[0].center_x)
    return [scene, jugador]
    
# Path = Path("assets") / "images" / "palanca1.png"
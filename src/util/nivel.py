# Herramienta tratamiento del Tilemap
from pathlib import Path
import json
import arcade
from entidad.jugador import Jugador
from util.camara import Camara

TILE_SCALING = 1

"""BASE_DIR = Path(__file__).resolve().parent.parent.parent

def _set_bloques(dict_bloques: dict, nivel:str) -> arcade.Scene:
    bloques = dict_bloques
    ruta = BASE_DIR / "assets" / "maps" / "bloques.json"
    with open (ruta, "w", newline="") as archivo:
        json.dump(bloques, archivo, indent=4, sort_keys=True)
    ruta = BASE_DIR / "assets" / "maps" / "bloques.json"
    tile_map = arcade.load_tilemap(
        ruta,
        scaling=TILE_SCALING,
        layer_options= _set_layer_options(bloques),
    ) 
    #print(tile_map.width*tile_map.tile_width)
    scene = arcade.Scene.from_tilemap(tile_map)
    return scene

def _set_layer_options(bloques:dict):
        layer_options = {}
        for layer in bloques["layers"]:
            if(layer["name"] == "Muros"):
                layer_options[layer["name"]] = {"use_spatial_hash": True}
        #print(layer_options)
        return layer_options

def crear_nivel(nivel:str)-> arcade.Scene:
    ruta = BASE_DIR / "assets" / "maps" / str(nivel+".json")
    with open(ruta, 'r', encoding='utf-8') as archivo:
        dict_nivel = json.load(archivo)
        print(buscar_capa(dict_nivel, "Algo"))
        for layer in dict_nivel["layers"]:
            # Dibujar los bloques
            if layer["name"] == "Bloques":
                dict_bloques = dict_nivel
                dict_bloques["layers"] = buscar_capa(dict_bloques, "Bloques")["layers"]
                scene = _set_bloques(dict_bloques, nivel)
            if layer["name"] == "Entidades":
                for entidad in layer["layers"]:
                    if entidad["name"] == "Jugador":
                        marcador = entidad["objects"][0]
                        #print(marcador["x"], marcador["y"])
                        #jugador = Jugador(center_x=marcador["x"], center_y=marcador["y"])
                        jugador = Jugador(center_x=300, center_y=300)
                        #print(jugador)
                        #print(marcador["name"])
            #print(layer["name"])
            #for layer in layer["layers"]:
                #print("    - " + layer["name"])
        #scene.add_sprite("Jugador", jugador)
        #print(scene.get_sprite_list("Jugador")[0].center_x)
    return [scene, jugador]

def buscar_capa(dict_nivel: dict, nombre: str):
    encontrado = False
    i = 0
    resultado = []
    while not encontrado and i < len(dict_nivel["layers"]):
        layer = dict_nivel["layers"][i]
        if layer["name"] == nombre:
            resultado = layer
            encontrado = True
        else:
            if layer["type"] == "group":
                resultado = buscar_capa(layer, nombre)
                if resultado != []: encontrado = True
        i += 1
    return resultado"""

    
# Path = Path("assets") / "images" / "palanca1.png"

class Tilemap():
    def __init__(self, path: Path):
        with open(path, 'r', encoding='utf-8') as archivo:
            self.dict = json.load(archivo)
        
    # Método para obtener una capa específica
    def _layer(self, nombre, dict = None):
        if(dict == None): dict = self.dict
        encontrado = False
        i = 0
        resultado = []
        while not encontrado and i < len(dict["layers"]):
            layer = dict["layers"][i]
            if layer["name"] == nombre:
                resultado = layer
                encontrado = True
            else:
                if layer["type"] == "group":
                    resultado = self._layer(nombre, layer)
                    if resultado != []: encontrado = True
            i += 1
        return resultado
    
    # Obtener una lista con el nombre de todas las capas del diccionario
    def _layers(self, dict = None) -> list:
        if(dict == None): dict = self.dict
        layers = []
        for layer in dict["layers"]:
            layers.append(layer["name"])
        return layers
    
    
    # Método para crear un nivel desde un Tilemap

class Nivel(arcade.View):
    def __init__(self, map: Tilemap | Path):
        super().__init__()
        self.tilemap = map if (map.__class__ == Tilemap) else Tilemap(map)
        self.scene = None
        self.setup()

        """self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.shoot_pressed = False

        self.player_texture = None
        self.player_sprite = None
        self.tile_map = None
        self.scene = None
        self.camera = None
        self.gui_camera = None

        self.score = 0
        self.score_text = None
        self.end_of_map = 0
        self.reset_score = True

        self.can_shoot = False
        self.shoot_timer = 0"""



    
    def setup(self):
        self.scene = self.crear_nivel()
        self.jugador = self.scene.get_sprite_list("Jugador")[0]
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.jugador,
            walls=self.scene["Muros"],
            gravity_constant=1,
        )
        self.camera = Camara()
        self.camera.zoom = 1
        self.camera.right_border = 8000 #self.tile_map.width*18*0.5
        self.camera.top_border = 6000 #self.tile_map.height*18*0.5
    
    def crear_nivel(self) -> arcade.Scene:

        def _layer_options(dict) -> dict:
            layer_options = {}
            for layer in tilemap._layers(dict):
                if(layer == "Muros"):
                    layer_options[layer] = {"use_spatial_hash": True}
            return layer_options
        
        def _crear_escena(tilemap: Tilemap) -> arcade.Scene:
            bloques = tilemap.dict.copy()
            bloques["layers"] = tilemap._layer("Bloques")["layers"]
            ruta = Path("assets") / "maps" / "bloques.json"
            with open (ruta, "w", newline="") as archivo:
                json.dump(bloques, archivo, indent=4, sort_keys=True)
            tile_map = arcade.load_tilemap(
                ruta,
                scaling=TILE_SCALING,
                layer_options= _layer_options(bloques),
            ) 
            scene = arcade.Scene.from_tilemap(tile_map)
            return scene
        
        def _append_jugador(tilemap: Tilemap, scene: arcade.Scene):
            altura = tilemap.dict["height"] * tilemap.dict["tileheight"]
            jugador_dict = tilemap._layer("Jugador")
            print(jugador_dict)
            for objeto in jugador_dict["objects"]:
                if objeto["type"] == "Jugador":
                    jugador = Jugador(center_x=objeto["x"], center_y=altura - objeto["y"])
            scene.add_sprite("Jugador", jugador)
        
        tilemap = self.tilemap
        scene = _crear_escena(tilemap)
        _append_jugador(tilemap, scene)
        return scene
    
    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()
    
    def on_update(self, delta_time):
        self.jugador.update(delta_time)
        self.physics_engine.update()
        self.camera.position = self.jugador.position

        self.camera.on_update()

        
    

    

    


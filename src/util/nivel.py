# Herramienta tratamiento del Tilemap
"""from pathlib import Path
import json
import arcade
from entidad.jugador import Jugador
from entidad.goblin_perseguidor import GoblinPerseguidor
from util.camara import Camara
from tile.puerta import Puerta
from tile.palanca import Palanca
from typing import Callable

TILE_SCALING = 1
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
    
    def _mayor_id(self, dict = None) -> int:
        max = -1
        if(dict == None): dict = self.dict
        if "layers" in dict.keys():
            for layer in dict["layers"]:
                if layer["id"] > max: max = layer["id"]
        elif "objects" in dict.keys():
            for object in dict["objects"]:
                if object["id"] > max: max = object["id"]
        return max
    
    
    # Método para crear un nivel desde un Tilemap

class Nivel(arcade.View):
    def __init__(self, map: Tilemap | Path):
        super().__init__()
        self.tilemap = map if (map.__class__ == Tilemap) else Tilemap(map)
        self.scene = None
        self.setup()

    def setup(self):
        self.scene = self.crear_nivel()
        self.jugador = self.scene.get_sprite_list("Jugador")[0]
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.jugador,
            walls=self.scene["Muros"],
            gravity_constant=0.8,
        )
        self.camera = Camara()
        self.camera.right_border = 8000 #self.tile_map.width*18*0.5
        self.camera.top_border = 6000 #self.tile_map.height*18*0.5
    
    def crear_nivel(self) -> arcade.Scene:

        #-----------------------------------------------------------------------------------------------------------------#
        def _crear_escena(tilemap: Tilemap) -> arcade.Scene:

            def _layer_options(dict) -> dict:
                layer_options = {}
                for layer in tilemap._layers(dict):
                    if(layer == "Muros"):
                        layer_options[layer] = {"use_spatial_hash": True}
                return layer_options
            
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
            for objeto in jugador_dict["objects"]:
                if objeto["type"] == "Jugador":
                    jugador = Jugador(scale=objeto["height"]/64, center_x=objeto["x"], center_y=altura - objeto["y"], distancia_al_suelo=5, muros=scene["Muros"])
                    enemigo = GoblinPerseguidor(jugador, scene["Muros"], scale=objeto["height"]/64, center_x=objeto["x"] + 100, center_y=altura - objeto["y"] + 600, distancia_al_suelo=5)
            scene.add_sprite("Jugador", jugador)
            scene.add_sprite("GoblinPerseguidor", enemigo)

        def _append_objetos(tilemap: Tilemap, scene: arcade.Scene):

            def _append_objetos_evento(tilemap: Tilemap, scene: arcade.Scene):
                altura = tilemap.dict["height"] * tilemap.dict["tileheight"]

                receptores = [None]*tilemap._mayor_id(tilemap._layer("Receptor"))
                scene.add_sprite("Receptor", arcade.Sprite())
                for objeto in tilemap._layer("Receptor")["objects"]:
                    print(objeto["name"])
                    if objeto["type"] == "Puerta":
                        puerta = Puerta(scale=objeto["height"]/64, center_x=objeto["x"], center_y=altura - objeto["y"] + objeto["height"]/2, name=objeto["name"])
                        scene.get_sprite_list("Receptor").append(puerta)
                        receptores.insert(objeto["id"], puerta)
                
                scene.add_sprite("Emisor", arcade.Sprite())
                for objeto in tilemap._layer("Emisor")["objects"]:
                    print(objeto["name"])
                    if objeto["type"] == "Palanca":
                        palanca = Palanca(interaccion1= receptores[objeto["properties"][0]["value"]].abrir, 
                                          interaccion2= receptores[objeto["properties"][0]["value"]].cerrar,
                                          scale=objeto["height"]/64, 
                                          center_x=objeto["x"], 
                                          center_y=altura - objeto["y"] + objeto["height"]/2)
                        print(receptores[objeto["properties"][0]["value"]].name)
                        scene.add_sprite("Emisor", palanca)
                print(scene.get_sprite_list("Receptor").pop(0))
                print(receptores)

            _append_objetos_evento(tilemap, scene)
        #-----------------------------------------------------------------------------------------------------------------#

        #-------------------------------#
        tilemap = self.tilemap
        scene = _crear_escena(tilemap)
        _append_jugador(tilemap, scene)
        if(tilemap._layer("Objetos") != []):
            _append_objetos(tilemap, scene)
        #-------------------------------#
        return scene
    
    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw(pixelated=True)
    
    def on_update(self, delta_time):
        self.scene.update(delta_time, ["Jugador", "GoblinPerseguidor"])
        self.scene.update_animation(delta_time, ["Jugador", "GoblinPerseguidor"])

        self.physics_engine.player_sprite = self.jugador
        self.physics_engine.update()

        for enemigo in self.scene["GoblinPerseguidor"]:
            # enemigo.change_y -= self.physics_engine.gravity_constant
            self.physics_engine.player_sprite = enemigo
            self.physics_engine.update()

        player_collision_list = arcade.check_for_collision_with_lists(
            self.jugador,
            [
                self.scene["Emisor"]
            ]
        )
        for collision in player_collision_list:
            print(collision)
            if self.scene["Emisor"] in collision.sprite_lists:
                print(collision)
                collision.on_collide(self.jugador)
        self.camera.position = self.jugador.position


        self.camera.on_update()"""

        
    

    
# Herramienta tratamiento del Tilemap
from pathlib import Path
import math
import random
import json
import arcade
from entidad.jugador import Jugador
from util.camara import Camara
from tile.puerta import Puerta, PuertaGris, PuertaNegra, Llave
from tile.palanca import Palanca
from typing import Callable
from menu.menu_principal import MenuPrincipal

TILE_SCALING = 1
class Tilemap():
    def __init__(self, path: Path):
        with open(path, 'r', encoding='utf-8') as archivo:
            self.dict = json.load(archivo)
        self.width = self.dict["width"]
        self.height = self.dict["height"]
        
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
    
    def _this_layers(self) -> list:
        dict = self.dict
        layers = []
        for layer in dict["layers"]:
            if(layer["type"] == "group"):
                for i in layer["layers"]:
                    layers.append(i["name"])
            else: layers.append(layer["name"])
        return layers
    
    def _mayor_id(self, dict = None) -> int:
        max = -1
        if(dict == None): dict = self.dict
        if "layers" in dict.keys():
            for layer in dict["layers"]:
                if layer["id"] > max: max = layer["id"]
        elif "objects" in dict.keys():
            for object in dict["objects"]:
                if object["id"] > max: max = object["id"]
        return max
    
    
    # Método para crear un nivel desde un Tilemap

class Nivel(arcade.View):
    def __init__(self, map: Tilemap | Path):
        super().__init__()
        self.tilemap = map if (map.__class__ == Tilemap) else Tilemap(map)
        self.scene = None
        self.teclas_presionadas = {}
        self.setup()

    def setup(self):
        self.scene = self.crear_nivel()
        self.jugador = self.scene.get_sprite_list("Jugador")[0]
        self.muros = self.scene["Muros"]
        self.plataformas_coladizas = self.scene["Plataformas Coladizas"]
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.jugador,
            walls=[self.muros, self.scene["Receptor"]],
            gravity_constant=1,
        )
        self.camera = Camara()
        self.camera.right_border = self.tilemap.width*64
        self.camera.top_border = self.tilemap.height*64
    
    def crear_nivel(self) -> arcade.Scene:
        #Crear escena
        def _crear_escena(tilemap: Tilemap) -> arcade.Scene:
            #Crear layer options
            def _layer_options(dict) -> dict:
                layer_options = {}
                for layer in tilemap._layers(dict):
                    if(layer == "Muros"):
                        layer_options[layer] = {"use_spatial_hash": True}
                return layer_options
            #Crear escena

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
            if(tilemap._layer("Jugador") != []):
                altura = tilemap.dict["height"] * tilemap.dict["tileheight"]
                jugador_dict = tilemap._layer("Jugador")
                for objeto in jugador_dict["objects"]:
                    if objeto["type"] == "Jugador":
                        jugador = Jugador(scale=objeto["height"]/64, center_x=objeto["x"], center_y=altura - objeto["y"], distancia_al_suelo=0, muros=scene.get_sprite_list("Muros"))
                scene.add_sprite("Jugador", jugador)

        def _append_objetos(tilemap: Tilemap, scene: arcade.Scene):
            #Objetos de evento
            def _append_objetos_evento(tilemap: Tilemap, scene: arcade.Scene):
                altura = tilemap.dict["height"] * tilemap.dict["tileheight"]

                receptores = [None]*tilemap._mayor_id(tilemap._layer("Receptor"))
                scene.add_sprite("Receptor", arcade.Sprite())
                for objeto in tilemap._layer("Receptor")["objects"]:
                    print(objeto["name"])
                    if objeto["type"] == "Puerta":
                        puerta = Puerta(scale=objeto["height"]/64, center_x=objeto["x"], center_y=altura - objeto["y"] + objeto["height"]/2, name=objeto["name"])
                        scene.get_sprite_list("Receptor").append(puerta)
                    elif objeto["type"] == "PuertaGris":
                        puerta = PuertaGris(change=objeto["properties"][0]["value"], scale=1, center_x=objeto["x"] + (-128 if objeto["rotation"] == -90.0 or objeto["rotation"] == 270 or abs(objeto["rotation"]) == 180 else 128),
                                            center_y=altura + - objeto["y"] + (objeto["height"]/2)*(-1 if objeto["rotation"] == 90 or objeto["rotation"] == -270 or abs(objeto["rotation"]) == 180 else 1), 
                                            angle=objeto["rotation"], name=objeto["name"])
                        scene.get_sprite_list("Receptor").append(puerta)
                    elif objeto["type"] == "PuertaNegra":
                        puerta = PuertaNegra(scale=1, center_x=objeto["x"] + (-96 if objeto["rotation"] == -90.0 or objeto["rotation"] == 270 or abs(objeto["rotation"]) == 180 else 105),
                                            center_y=altura + - objeto["y"] + (105 if objeto["rotation"] == -90 or objeto["rotation"] == -270 or abs(objeto["rotation"]) == 180 else 96), 
                                            angle=objeto["rotation"], name=objeto["name"])
                        scene.get_sprite_list("Receptor").append(puerta)
                    receptores.insert(objeto["id"], puerta)
                
                scene.add_sprite("Emisor", arcade.Sprite())
                for objeto in tilemap._layer("Emisor")["objects"]:
                    print(objeto["name"])
                    if objeto["type"] == "Palanca":
                        if objeto["properties"][1]["value"] == "false":
                            interaccion1 = []
                            for receptor in objeto["properties"][2]["value"]:
                                interaccion1.append(receptores[receptor["value"]].abrir)
                            interaccion2 = []
                            for receptor in objeto["properties"][2]["value"]:
                                interaccion2.append(receptores[receptor["value"]].cerrar)
                            palanca = Palanca(interaccion1= interaccion1, 
                                            interaccion2= interaccion2,
                                            scale=objeto["height"]/64, 
                                            center_x=objeto["x"] + objeto["width"]/2, 
                                            center_y=altura - objeto["y"] + objeto["height"]/2)
                            scene.add_sprite("Emisor", palanca)
                        else: 
                            print("Hola")
                            recs = [r for r in objeto["properties"][2]["value"] if receptores[r["value"]] is not None]
                            random.shuffle(recs)
                            cont = 0
                            i = 0
                            interaccion1 = []
                            interaccion2 = []
                            while cont < 2 and i < len(recs):
                                rec_obj = recs[i]["value"]
                                interaccion1.append(receptores[rec_obj].abrir)
                                interaccion2.append(receptores[rec_obj].cerrar)
                                receptores[rec_obj] = None
                                cont += 1
                                i +=1
                            palanca = Palanca(interaccion1= interaccion1, 
                                            interaccion2= interaccion2,
                                            scale=objeto["height"]/64, 
                                            center_x=objeto["x"] + objeto["width"]/2, 
                                            center_y=altura - objeto["y"] + objeto["height"]/2)
                            scene.add_sprite("Emisor", palanca)
                print(scene.get_sprite_list("Receptor").pop(0))
                print(receptores)

            def _append_llaves(tilemap: Tilemap, scene: arcade.Scene):
                altura = tilemap.dict["height"] * tilemap.dict["tileheight"]
                scene.add_sprite("Llave", arcade.Sprite())
                if(tilemap._layer != []):
                    if tilemap._layer("Llave")["properties"][0]["value"] == True:
                        posiciones = []
                        for objeto in tilemap._layer("Llave")["objects"]:
                            if objeto["type"] == "Llave":
                                posiciones.append(objeto)
                        random.shuffle(posiciones)
                        objeto = posiciones[0]
                        llave = Llave(scale=objeto["height"]/64, center_x=objeto["x"] + objeto["width"]/2, center_y=altura - objeto["y"] + objeto["height"]/2, name=objeto["name"])
                        scene.get_sprite_list("Llave").append(llave)
                        
            _append_objetos_evento(tilemap, scene)
            _append_llaves(tilemap, scene)

        tilemap = self.tilemap
        layers = tilemap._this_layers()
        # Identificamos las capas que tenemos que tratar
        scene = _crear_escena(tilemap)
        _append_jugador(tilemap, scene)
        _append_objetos(tilemap, scene)
        return scene
    
    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()
    
    def on_update(self, delta_time):
        self.jugador.update(delta_time)

        self.physics_engine.update()
        colisiones_plataformas = arcade.check_for_collision_with_list(self.jugador, self.plataformas_coladizas)
        
        if self.jugador.change_y <= 0 and colisiones_plataformas:
            plataforma_objetivo = max(colisiones_plataformas, key = lambda p: p.top)
            if self.jugador.bottom > plataforma_objetivo.top -20 and not self.teclas_presionadas.get(arcade.key.S, False):
                self.jugador.bottom = plataforma_objetivo.top + 0.8
                self.jugador.change_y = 0

        
        if self.puedo_saltar():
            self.jugador._can_jump = True
            self._en_muro = False
            self._en_suelo = True
            self._ultimo_muro_saltado = 0
            self.jugador._contador_salto_muro = -1
        else: 
            self.jugador._can_jump = False
        player_collision_list = arcade.check_for_collision_with_lists(
            self.jugador,
            [
                self.scene["Emisor"]
            ]
        )
        for collision in player_collision_list:
            print(collision)
            if self.scene["Emisor"] in collision.sprite_lists:
                print(collision)
                collision.on_collide(self.jugador)
        
        player_collision_list = arcade.check_for_collision_with_lists(
            self.jugador,
            [
                self.scene["Llave"]
            ]
        )
        for collision in player_collision_list:
            if self.scene["Llave"] in collision.sprite_lists:
                print(collision)
                collision.visible = False
                collision.center_x = -10000
                collision.center_y = -10000
                self.window.show_view(MenuPrincipal())
        self.camera.position = self.jugador.position


        self.camera.on_update()

    def on_key_press(self, key, modifiers):
        self.teclas_presionadas[key] = True

    def on_key_release(self, key, modifiers):
        self.teclas_presionadas[key] = False
    
    def puedo_saltar(self):
        if self.physics_engine.can_jump():
            return True
        plataforma_objetivo = min(self.scene.get_sprite_list("Plataformas Coladizas"), key = lambda p: arcade.get_distance_between_sprites(self.jugador, p))
        if self.jugador.bottom >= plataforma_objetivo.top - 5:
            return True
        return False


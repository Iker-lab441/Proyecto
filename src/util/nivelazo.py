# Herramienta tratamiento del Tilemap
from pathlib import Path
import random
import json
import arcade
from entidad.jugador import Jugador
from entidad.goblin_perseguidor import GoblinPerseguidor
from entidad.proyectil import Proyectil
from util.camara import Camara
from tile.puerta import Puerta, PuertaGris, PuertaNegra, Llave, PuertaSalida
from tile.palanca import Palanca
from typing import Any, Callable
import util.globales
from menu.menu_principal import MenuPrincipal

TILE_SCALING = 1

CAPA_MUROS = "Muros"
CAPA_PLATAFORMAS_COLADIZAS = "Plataformas Coladizas"
CAPA_JUGADOR = "Jugador"
CAPA_GOBLIN = "Goblin"
CAPA_EMISOR = "Emisor"
CAPA_RECEPTOR = "Receptor"
CAPA_LLAVE = "Llave"
CAPA_SALIDA = "Salida"
CAPA_PROYECTIL = "Proyectil"

class Tilemap():
    def __init__(self, path: Path):
        with open(path, 'r', encoding='utf-8') as archivo:
            self.dict: dict[str, Any] = json.load(archivo)
        self.width = self.dict["width"]
        self.height = self.dict["height"]

    # Método para obtener una capa específica
    def _layer(self, nombre: str, diccionario: dict[str, Any] | None = None) -> dict[str, Any] | None:
        if diccionario is None:
            diccionario = self.dict

        layers: list[Any] = diccionario["layers"]

        for layer in layers:
            if layer["name"] == nombre:
                return layer
            elif layer["type"] == "group":
                resultado = self._layer(nombre, layer)
                if resultado != None:
                    return resultado

        return None

    # Obtener una lista con el nombre de todas las capas del diccionario
    def _layers(self, diccionario: dict[str, Any] | None = None) -> list[str]:
        if diccionario is None:
            diccionario = self.dict

        # print("DICT: ", diccionario, " :TCID")
        return [layer["name"] for layer in diccionario["layers"]]

    def _this_layers(self) -> list[str]:
        layers: list[str] = []

        for layer in self.dict["layers"]:
            if(layer["type"] == "group"):
                for nombre in layer:
                    layers.append(nombre)
            else: layers.append(layer["name"])

        return layers

    def _mayor_id(self, diccionario: dict[str, Any] | None = None) -> int:
        if diccionario is None:
            diccionario = self.dict

        max = -1

        if "layers" in diccionario.keys():
            for layer in diccionario["layers"]:
                if layer["id"] > max:
                    max = layer["id"]
        elif "objects" in diccionario.keys():
            for object in diccionario["objects"]:
                if object["id"] > max:
                    max = object["id"]

        return max


    # Método para crear un nivel desde un Tilemap

class Nivel(arcade.View):
    def __init__(self, map: Tilemap | Path):
        super().__init__()
        self.tilemap: Tilemap = map if isinstance(map, Tilemap) else Tilemap(map)
        self.scene: arcade.Scene
        self.jugador: Jugador
        self.muros: arcade.SpriteList[arcade.Sprite]
        self.plataformas_coladizas: arcade.SpriteList[arcade.Sprite]
        self.physics_engine: arcade.PhysicsEnginePlatformer
        self.teclas_presionadas = {} # TODO: eliminar
        self.setup()

    def setup(self):
        self.scene = self.crear_nivel()
        self.jugador = self.scene[CAPA_JUGADOR][0]
        assert(isinstance(self.jugador, Jugador))
        self.muros = self.scene[CAPA_MUROS]
        self.plataformas_coladizas = self.scene[CAPA_PLATAFORMAS_COLADIZAS]
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.jugador,
            walls=[self.muros, self.scene[CAPA_RECEPTOR]],
            gravity_constant=1,
        )
        self.camera = Camara()
        self.camera.right_border = self.tilemap.width*64
        self.camera.top_border = self.tilemap.height*64

        util.globales.nivel = self
        util.globales.jugador = self.jugador
        util.globales.paredes = self.muros

        for muro in self.muros:
            util.globales.suelos.append(muro)

        for suelo in self.plataformas_coladizas:
            util.globales.suelos.append(suelo)

    def crear_nivel(self) -> arcade.Scene:
        #Crear escena
        def _crear_escena(tilemap: Tilemap) -> arcade.Scene:
            #Crear layer options
            def _layer_options(diccionario: dict[str, Any]) -> dict[str, dict[str, bool]]:
                layer_options: dict[str, dict[str, bool]] = {}

                for layer in tilemap._layers(diccionario):
                    if layer == CAPA_MUROS:
                        layer_options[layer] = {"use_spatial_hash": True}

                return layer_options
            #Crear escena

            layer_bloques = tilemap._layer("Bloques")
            assert(layer_bloques is not None)

            bloques = tilemap.dict.copy()
            bloques["layers"] = layer_bloques["layers"]

            ruta = Path("assets") / "maps" / "bloques.json"
            with open (ruta, "w", newline="") as archivo:
                json.dump(bloques, archivo, indent=4, sort_keys=True)

            tile_map = arcade.load_tilemap(
                ruta,
                scaling=TILE_SCALING,
                layer_options= _layer_options(bloques),
            ) 

            return arcade.Scene.from_tilemap(tile_map)

        def _append_jugador(tilemap: Tilemap, scene: arcade.Scene):
            layer_jugador = tilemap._layer(CAPA_JUGADOR)
            assert(layer_jugador is not None)

            altura = tilemap.dict["height"] * tilemap.dict["tileheight"]

            for objeto in layer_jugador["objects"]:
                if objeto["type"] == "Jugador":
                    jugador = Jugador(scale=objeto["height"] / 64, center_x=objeto["x"], center_y=altura - objeto["y"])
                    scene.add_sprite(CAPA_JUGADOR, jugador)

        def _append_goblins(tilemap: Tilemap, scene: arcade.Scene):
            layer_goblins = tilemap._layer(CAPA_GOBLIN)
            assert(layer_goblins is not None)

            altura = tilemap.dict["height"] * tilemap.dict["tileheight"]
            print(f"{altura = }")

            scene.add_sprite(CAPA_GOBLIN, arcade.Sprite())

            for objeto in layer_goblins["objects"]:
                if objeto["type"] == "GoblinPerseguidor":
                    goblin = GoblinPerseguidor(scale=objeto["height"] / 64, center_x=objeto["x"], center_y=altura - objeto["y"] + tilemap.dict["tileheight"])
                    print(f"{objeto['y'] = }")
                    scene.add_sprite(CAPA_GOBLIN, goblin)

        def _append_objetos(tilemap: Tilemap, scene: arcade.Scene):
            #Objetos de evento
            def _append_objetos_evento(tilemap: Tilemap, scene: arcade.Scene):
                altura = tilemap.dict["height"] * tilemap.dict["tileheight"]

                receptores: list[arcade.Sprite | None] = [None] * (tilemap._mayor_id(tilemap._layer(CAPA_RECEPTOR)) + 1)
                scene.add_sprite(CAPA_RECEPTOR, arcade.Sprite())

                layer_receptor = tilemap._layer(CAPA_RECEPTOR)
                assert(layer_receptor is not None)

                for objeto in layer_receptor["objects"]:
                    print(objeto["name"])
                    puerta = None

                    match objeto["type"]:
                        case "Puerta":
                            puerta = Puerta(scale=objeto["height"] / 64, center_x=objeto["x"], center_y=altura - objeto["y"] + objeto["height"] / 2, name=objeto["name"])
                            scene.add_sprite(CAPA_RECEPTOR, puerta)
                        case "PuertaGris":
                            puerta = PuertaGris(change=objeto["properties"][0]["value"], scale=1, center_x=objeto["x"] + (-128 if objeto["rotation"] == -90.0 or objeto["rotation"] == 270 or abs(objeto["rotation"]) == 180 else 128),
                                                center_y=altura + - objeto["y"] + (objeto["height"]/2)*(-1 if objeto["rotation"] == 90 or objeto["rotation"] == -270 or abs(objeto["rotation"]) == 180 else 1), 
                                                angle=objeto["rotation"], name=objeto["name"])
                            scene.add_sprite(CAPA_RECEPTOR, puerta)
                        case "PuertaNegra":
                            puerta = PuertaNegra(scale=1, center_x=objeto["x"] + (-96 if objeto["rotation"] == -90.0 or objeto["rotation"] == 270 or abs(objeto["rotation"]) == 180 else 105),
                                                center_y=altura + - objeto["y"] + (105 if objeto["rotation"] == -90 or objeto["rotation"] == -270 or abs(objeto["rotation"]) == 180 else 96), 
                                                angle=objeto["rotation"], name=objeto["name"])
                            scene.add_sprite(CAPA_RECEPTOR, puerta)
                        case _:
                            pass

                    if puerta:
                        receptores[objeto["id"]] = puerta
                
                scene.add_sprite(CAPA_EMISOR, arcade.Sprite())

                layer_emisor = tilemap._layer(CAPA_EMISOR)
                assert(layer_emisor is not None)

                for objeto in layer_emisor["objects"]:
                    print(objeto["name"])

                    match objeto["type"]:
                        case "Palanca":
                            if objeto["properties"][1]["value"] == "false":
                                interaccion1: list[Callable[..., None]] = [receptores[receptor["value"]].abrir for receptor in objeto["properties"][2]["value"]]
                                interaccion2: list[Callable[..., None]] = [receptores[receptor["value"]].cerrar for receptor in objeto["properties"][2]["value"]]

                                palanca = Palanca(interaccion1, 
                                                interaccion2,
                                                scale=objeto["height"] / 64, 
                                                center_x=objeto["x"] + objeto["width"] / 2, 
                                                center_y=altura - objeto["y"] + objeto["height"] / 2)

                                scene.add_sprite(CAPA_EMISOR, palanca)
                                print("HEREEEEEEEEEEEEEEEE")
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
                                scene.add_sprite(CAPA_EMISOR, palanca)
                        case _:
                            pass
                print(scene.get_sprite_list(CAPA_RECEPTOR).pop(0))
                print(receptores)

            def _append_llaves(tilemap: Tilemap, scene: arcade.Scene):
                altura = tilemap.dict["height"] * tilemap.dict["tileheight"]

                scene.add_sprite(CAPA_LLAVE, arcade.Sprite())

                layer_llave = tilemap._layer(CAPA_LLAVE)
                if layer_llave is not None:
                    if layer_llave["properties"][0]["value"] == True:
                        posiciones = []
                        for objeto in layer_llave["objects"]:
                            if objeto["type"] == CAPA_LLAVE:
                                posiciones.append(objeto)
                        random.shuffle(posiciones)
                        if posiciones:
                            objeto = posiciones[0]
                            llave = Llave(scale=objeto["height"] / 64, center_x=objeto["x"] + objeto["width"] / 2, center_y=altura - objeto["y"] + objeto["height"] / 2, name=objeto["name"])
                            scene.add_sprite(CAPA_LLAVE, llave)

            def _append_salida(tilemap: Tilemap, scene: arcade.Scene):
                altura = tilemap.dict["height"] * tilemap.dict["tileheight"]

                scene.add_sprite(CAPA_SALIDA, arcade.Sprite())

                layer_salida = tilemap._layer(CAPA_SALIDA)
                if layer_salida is not None:
                    for objeto in layer_salida["objects"]:
                        if objeto["type"] == "PuertaSalida":
                            puerta = PuertaSalida(scale=objeto["height"] / 64, center_x=objeto["x"] + objeto["width"] / 2, center_y=altura - objeto["y"] + objeto["height"] / 2, name=objeto["name"])
                            scene.add_sprite(CAPA_SALIDA, puerta)
                        if objeto["type"] == "PuertaEntrada":
                            puerta = arcade.Sprite(path_or_texture=Path("assets") / "images" / "puerta_abierta_fondo.png", scale=objeto["height"]/64, center_x=objeto["x"] + objeto["width"]/2, center_y=altura - objeto["y"] + objeto["height"]/2)
                            scene.add_sprite(CAPA_SALIDA, puerta)

            _append_objetos_evento(tilemap, scene)
            _append_llaves(tilemap, scene)
            _append_salida(tilemap, scene)

        tilemap = self.tilemap
        layers = tilemap._this_layers()
        # Identificamos las capas que tenemos que tratar
        scene = _crear_escena(tilemap)

        _append_objetos(tilemap, scene)
        _append_goblins(tilemap, scene)
        _append_jugador(tilemap, scene)
        scene.add_sprite_list(CAPA_PROYECTIL)

        return scene

    def add_proyectil(self, proyectil: Proyectil) -> None:
        self.scene.add_sprite(CAPA_PROYECTIL, proyectil)

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw(pixelated=True)
    
    def on_update(self, delta_time: float):
        self.scene.update(delta_time, [CAPA_JUGADOR, CAPA_GOBLIN, CAPA_PROYECTIL])
        self.scene.update_animation(delta_time, [CAPA_JUGADOR, CAPA_GOBLIN, CAPA_PROYECTIL])

        for goblin in self.scene[CAPA_GOBLIN]:
            self.physics_engine.player_sprite = goblin
            self.physics_engine.update()

        self.physics_engine.player_sprite = self.jugador
        self.physics_engine.update()

        colisiones_plataformas = arcade.check_for_collision_with_list(self.jugador, self.plataformas_coladizas)
        
        if self.jugador.change_y <= 0 and colisiones_plataformas:
            plataforma_objetivo = max(colisiones_plataformas, key = lambda p: p.top)
            if self.jugador.bottom > plataforma_objetivo.top -20 and not self.teclas_presionadas.get(arcade.key.S, False):
                self.jugador.bottom = plataforma_objetivo.top + 0.8
                self.jugador.change_y = 0

        player_collision_list = arcade.check_for_collision_with_lists(
            self.jugador,
            [
                self.scene[CAPA_EMISOR]
            ]
        )
        for collision in player_collision_list:
            print(collision)
            if self.scene[CAPA_EMISOR] in collision.sprite_lists:
                print(collision)
                collision.on_collide(self.jugador)
        
        player_collision_list = arcade.check_for_collision_with_lists(
            self.jugador,
            [
                self.scene[CAPA_LLAVE]
            ]
        )
        for collision in player_collision_list:
            if self.scene[CAPA_LLAVE] in collision.sprite_lists:
                print(collision)
                collision.visible = False
                collision.center_x = -10000
                collision.center_y = -10000
                self.jugador._has_llave = True

        player_collision_list = arcade.check_for_collision_with_lists(
            self.jugador,
            [
                self.scene[CAPA_SALIDA]
            ]
        )
        for collision in player_collision_list:
            if self.scene[CAPA_SALIDA] in collision.sprite_lists:
                print(collision)
                if isinstance(collision, PuertaSalida):
                    if(collision.on_collide(self.jugador)):
                        self.window.show_view(MenuPrincipal())
        self.camera.position = self.jugador.position


        self.camera.on_update()

    def on_key_press(self, key, modifiers):
        self.teclas_presionadas[key] = True

    def on_key_release(self, key, modifiers):
        self.teclas_presionadas[key] = False

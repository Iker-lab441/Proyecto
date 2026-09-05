# Herramienta tratamiento del Tilemap
from pathlib import Path
import random
import json
import arcade
from entidad.jugador import Jugador
from entidad.goblin_perseguidor import GoblinPerseguidor
from entidad.goblin_disparador import GoblinDisparador
from entidad.proyectil import Proyectil
from entidad.flecha import Flecha
from entidad.lucian import Lucian
from util.interfaz import InterfazNivel
from util import texturas
from util.camara import Camara
from tile.puerta import Puerta, PuertaGris, PuertaNegra, Llave, PuertaSalida
from tile.palanca import Palanca
from tile.boton import Boton
from typing import Any, Callable
import util.globales
import util.io
from config import controles

TILE_SCALING = 1

CAPA_BLOQUES = "Bloques"
CAPA_MUROS = "Muros"
CAPA_PLATAFORMAS_COLADIZAS = "Plataformas Coladizas"
CAPA_JUGADOR = "Jugador"
CAPA_LUCIAN = "Lucian"
CAPA_GOBLIN = "Goblin"
CAPA_EMISOR = "Emisor"
CAPA_RECEPTOR = "Receptor"
CAPA_RECEPTOR_PUERTA_ABIERTA = "ReceptorPuertaAbierta"
CAPA_LLAVE = "Llave"
CAPA_SALIDA = "Salida"
CAPA_PROYECTIL = "Proyectil"

_MUSICA_POR_MAPA: dict[str, str] = {
    "laberinto":        "musica_nivel_1",
    "minijuego":        "musica_tutorial",
    "parkour":          "musica_rapida",
    "nivel_final":      "musica_rapida",
    "jefe_final":       "musica_boss",
    "test_salto_pared": "musica_tutorial",
}
_MUSICA_DEFAULT = "musica_nivel_1"

class Tilemap():
    def __init__(self, path: Path):
        with open(path, 'r', encoding='utf-8') as archivo:
            self.dict: dict[str, Any] = json.load(archivo)

        self.width = self.dict["width"]
        self.height = self.dict["height"]
        self.path = path

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

        return [layer["name"] for layer in diccionario["layers"]]

    def _this_layers(self) -> list[str]:
        layers: list[str] = []

        for layer in self.dict["layers"]:
            if layer["type"] == "group":
                for nombre in layer:
                    layers.append(nombre)
            else:
                layers.append(layer["name"])

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
    def __new__(cls, map: Path) -> "Nivel":
        if map.stem == "minijuego":
            return Minijuego(map)

        return super().__new__(cls)

    def __init__(self, map: Path):
        super().__init__()
        self.path_mapa: Path
        self.tilemap: Tilemap
        self.scene: arcade.Scene
        self.jugador: Jugador
        self.muros: arcade.SpriteList[arcade.Sprite]
        self.plataformas_coladizas: arcade.SpriteList[arcade.Sprite]
        self.interfaz: InterfazNivel
        self.physics_engine: arcade.PhysicsEnginePlatformer
        self.dialogo_acabado: bool
        self.setup(map)

        self.dialogo_acabado = True
        self.on_update(1 / 60)
        self.dialogo_acabado = False

    def setup(self, map: Path):
        with open("save.txt", "w") as archivo_guardado:
            archivo_guardado.write(map.stem)

        self.path_mapa = map
        self.tilemap: Tilemap = Tilemap(self.path_mapa)
        self.scene = self.crear_nivel()
        self.jugador = self.scene[CAPA_JUGADOR][0]
        assert(isinstance(self.jugador, Jugador))
        self.muros = self.scene[CAPA_MUROS]
        self.plataformas_coladizas = self.scene[CAPA_PLATAFORMAS_COLADIZAS] if CAPA_PLATAFORMAS_COLADIZAS in self.scene else arcade.SpriteList()
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.jugador,
            walls=[self.muros, self.scene[CAPA_RECEPTOR]],
            gravity_constant=1,
        )
        self.camera = Camara()
        self.camera.zoom = 0.5 if self.path_mapa.stem == "laberinto" else 1
        self.camera.right_border = self.tilemap.width * 64
        self.camera.top_border = self.tilemap.height * 64
        self.dialogo_acabado = False

        self.interfaz = InterfazNivel(self.window.width, self.window.height, Path("assets") / "dialogs" / (self.path_mapa.stem + ".txt"))

        util.globales.nivel = self
        util.globales.jugador = self.jugador
        util.globales.paredes = self.muros
        util.globales.suelos = arcade.SpriteList()

        for muro in self.muros:
            util.globales.suelos.append(muro)

        for suelo in self.plataformas_coladizas:
            util.globales.suelos.append(suelo)
        
        clave_musica = _MUSICA_POR_MAPA.get(self.path_mapa.stem, _MUSICA_DEFAULT)
        util.globales.audio.reproducir_musica(clave_musica)

    def _append_objetos_evento(self, tilemap: Tilemap, scene: arcade.Scene):
        scene.add_sprite_list(CAPA_RECEPTOR)
        scene.add_sprite_list(CAPA_EMISOR)
        scene.add_sprite_list(CAPA_RECEPTOR_PUERTA_ABIERTA)

        layer_receptor = tilemap._layer(CAPA_RECEPTOR)

        if layer_receptor is None:
            return

        altura = tilemap.dict["height"] * tilemap.dict["tileheight"]
        receptores: list[arcade.Sprite | None] = [None] * (tilemap._mayor_id(tilemap._layer(CAPA_RECEPTOR)) + 1)

        for objeto in layer_receptor["objects"]:
            puerta = None

            match objeto["type"]:
                case "Puerta":
                    puerta = Puerta(capa_receptor=scene[CAPA_RECEPTOR], capa_receptor_puerta_abierta=scene[CAPA_RECEPTOR_PUERTA_ABIERTA], scale=objeto["height"] / 64, center_x=objeto["x"] + objeto["width"] / 2, center_y=altura - objeto["y"] + objeto["height"] / 2, name=objeto["name"])
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

            if puerta:
                receptores[objeto["id"]] = puerta

        layer_emisor = tilemap._layer(CAPA_EMISOR)

        if layer_emisor is None:
            return

        for objeto in layer_emisor["objects"]:
            match objeto["type"]:
                case "Palanca":
                    if objeto["properties"][1]["value"] is False:
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

            layer_bloques = tilemap._layer(CAPA_BLOQUES)
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
                    jugador = Jugador(scale=objeto["height"] / 64, center_x=objeto["x"] + tilemap.dict["tilewidth"], center_y=altura - objeto["y"] + tilemap.dict["tileheight"])
                    scene.add_sprite(CAPA_JUGADOR, jugador)

        def _append_goblins(tilemap: Tilemap, scene: arcade.Scene):
            scene.add_sprite_list(CAPA_GOBLIN)

            layer_goblins = tilemap._layer(CAPA_GOBLIN)

            if layer_goblins is None:
                return

            altura = tilemap.dict["height"] * tilemap.dict["tileheight"]
            print(f"{altura = }")

            for objeto in layer_goblins["objects"]:
                match objeto["type"]:
                    case "GoblinPerseguidor":
                        goblin = GoblinPerseguidor(scale=objeto["height"] / 64, center_x=objeto["x"] + tilemap.dict["tilewidth"], center_y=altura - objeto["y"] + tilemap.dict["tileheight"])
                        scene.add_sprite(CAPA_GOBLIN, goblin)
                    case "GoblinDisparador":
                        goblin = GoblinDisparador(scale=objeto["height"] / 64, center_x=objeto["x"] + tilemap.dict["tilewidth"], center_y=altura - objeto["y"] + tilemap.dict["tileheight"])
                        scene.add_sprite(CAPA_GOBLIN, goblin)

        def _append_lucian(tilemap: Tilemap, scene: arcade.Scene):
            scene.add_sprite_list(CAPA_LUCIAN)

            layer_lucian = tilemap._layer(CAPA_LUCIAN)
            if layer_lucian is None:
                return

            altura = tilemap.dict["height"] * tilemap.dict["tileheight"]

            objeto_lucian: dict[str, Any] | None = None

            print(layer_lucian)

            embestidas: dict[tuple[float, float], tuple[float, float]] = {}
            todas_las_embestidas: list[tuple[float, float] | None] = [None] * (tilemap._mayor_id(layer_lucian) + 1)

            posiciones_disparo: list[arcade.Vec2] = []

            caida_x: float = 0
            caida_y: float = 0
            distancia_lateral_caida: float = 0

            for objeto in layer_lucian["objects"]:
                match objeto["type"]:
                    case "Lucian":
                        objeto_lucian = objeto
                    case "Embestida":
                        id: int = objeto["id"]
                        embestida: tuple[float, float] = (objeto["x"] + tilemap.dict["tilewidth"] * 2, altura - objeto["y"] + tilemap.dict["tileheight"] * 2)
                        todas_las_embestidas[id] = embestida
                    case "Disparo":
                        posiciones_disparo.append(arcade.Vec2(objeto["x"] + tilemap.dict["tilewidth"] * 2, altura - objeto["y"] + tilemap.dict["tileheight"] * 2))
                    case "Caida":
                        caida_x = objeto["x"] + tilemap.dict["tilewidth"] * 2
                        caida_y = altura - objeto["y"] + tilemap.dict["tileheight"] * 2
                        distancia_lateral_caida = objeto["properties"][0]["value"] * tilemap.dict["tilewidth"]

            for objeto in layer_lucian["objects"]:
                if objeto["type"] == "Embestida":
                    id_objeto: int = objeto["id"]
                    id_asociado: int = objeto["properties"][0]["value"]

                    embestida_objeto = todas_las_embestidas[id_objeto]
                    embestida_asociada = todas_las_embestidas[id_asociado]

                    assert(embestida_objeto is not None)
                    assert(embestida_asociada is not None)

                    if embestida_asociada not in embestidas:
                        embestidas[embestida_objeto] = embestida_asociada

            if objeto_lucian is not None:
                lucian = Lucian(embestidas=embestidas, posiciones_disparo=posiciones_disparo, caida_x=caida_x, caida_y=caida_y, distancia_lateral_caida=distancia_lateral_caida,
                                scale=objeto_lucian["height"] / 64, center_x=objeto_lucian["x"] + tilemap.dict["tilewidth"] * 2, center_y=altura - objeto_lucian["y"] + tilemap.dict["tileheight"] * 2)
                scene.add_sprite(CAPA_LUCIAN, lucian)

        def _append_objetos(tilemap: Tilemap, scene: arcade.Scene):
            #Objetos de evento

            def _append_llaves(tilemap: Tilemap, scene: arcade.Scene):
                scene.add_sprite_list(CAPA_LLAVE)

                altura = tilemap.dict["height"] * tilemap.dict["tileheight"]
                layer_llave = tilemap._layer(CAPA_LLAVE)

                if layer_llave is None:
                    return

                if layer_llave["properties"][0]["value"] is True:
                    posiciones = [objeto for objeto in layer_llave["objects"] if objeto["type"]]
                    random.shuffle(posiciones)
                    if posiciones:
                        objeto = posiciones[0]
                        llave = Llave(scale=objeto["height"] / 64, center_x=objeto["x"] + objeto["width"] / 2, center_y=altura - objeto["y"] + objeto["height"] / 2, name=objeto["name"])
                        scene.add_sprite(CAPA_LLAVE, llave)

            def _append_salida(tilemap: Tilemap, scene: arcade.Scene):
                scene.add_sprite_list(CAPA_SALIDA)

                altura = tilemap.dict["height"] * tilemap.dict["tileheight"]
                layer_salida = tilemap._layer(CAPA_SALIDA)

                if layer_salida is None:
                    return

                for objeto in layer_salida["objects"]:
                    match objeto["type"]:
                        case "PuertaSalida":
                            puerta = PuertaSalida(siguiente_nivel=Path("assets") / "maps" / (objeto["properties"][0]["value"] + ".json"), scale=objeto["height"] / 64, center_x=objeto["x"] + objeto["width"] / 2, center_y=altura - objeto["y"] + objeto["height"] / 2, name=objeto["name"])
                            scene.add_sprite(CAPA_SALIDA, puerta)
                        case "PuertaEntrada":
                            puerta = arcade.Sprite(path_or_texture=texturas.Tiles.PUERTA_ABIERTA_FONDO, scale=objeto["height"]/64, center_x=objeto["x"] + objeto["width"]/2, center_y=altura - objeto["y"] + objeto["height"]/2) # TODO: convertir en clase
                            scene.add_sprite(CAPA_SALIDA, puerta)

            self._append_objetos_evento(tilemap, scene)
            _append_llaves(tilemap, scene)
            _append_salida(tilemap, scene)

        tilemap = self.tilemap
        # Identificamos las capas que tenemos que tratar
        scene = _crear_escena(tilemap)

        _append_objetos(tilemap, scene)
        _append_goblins(tilemap, scene)
        _append_lucian(tilemap, scene)
        _append_jugador(tilemap, scene)

        scene.add_sprite_list(CAPA_PROYECTIL)

        return scene

    def add_proyectil(self, proyectil: Proyectil) -> None:
        self.scene.add_sprite(CAPA_PROYECTIL, proyectil)
    
    def on_update(self, delta_time: float):
        self.scene.update_animation(delta_time, [CAPA_JUGADOR, CAPA_GOBLIN, CAPA_LUCIAN, CAPA_PROYECTIL, CAPA_EMISOR])

        if not self.dialogo_acabado and util.io.tecla_justo_soltada(controles.avanzar_dialogo):
            self.dialogo_acabado = not self.interfaz.avanzar_dialogo()

        if not self.dialogo_acabado:
            return

        self.scene.update(delta_time, [CAPA_JUGADOR, CAPA_GOBLIN, CAPA_LUCIAN, CAPA_PROYECTIL, CAPA_EMISOR])

        for goblin in self.scene[CAPA_GOBLIN]:
            if isinstance(goblin, GoblinPerseguidor):
                self.physics_engine.player_sprite = goblin
                self.physics_engine.update()

        for lucian in self.scene[CAPA_LUCIAN]:
            if isinstance(lucian, Lucian) and lucian.tiene_fisicas:
                self.physics_engine.player_sprite = lucian
                self.physics_engine.update()

        for proyectil in self.scene[CAPA_PROYECTIL]:
            # La flecha tiene gravedad, pero más ligera
            if isinstance(proyectil, Flecha):
                self.physics_engine.gravity_constant /= 3

                self.physics_engine.player_sprite = proyectil
                self.physics_engine.update()

                if self.physics_engine.can_jump():
                    proyectil.kill()

                self.physics_engine.gravity_constant *= 3

        self.physics_engine.player_sprite = self.jugador
        self.physics_engine.update()

        colisiones_plataformas = arcade.check_for_collision_with_list(self.jugador, self.plataformas_coladizas)
        
        if self.jugador.change_y <= 0 and colisiones_plataformas:
            plataforma_objetivo = max(colisiones_plataformas, key = lambda p: p.top)
            if self.jugador.bottom > plataforma_objetivo.top - 20 and not util.io.tecla_mantenida(controles.jugador_abajo):
                self.jugador.bottom = plataforma_objetivo.top + 0.8
                self.jugador.change_y = 0

        player_collision_list = arcade.check_for_collision_with_lists(
            self.jugador,
            [
                self.scene[CAPA_EMISOR],
                self.scene[CAPA_GOBLIN],
                self.scene[CAPA_LUCIAN]
            ]
        )

        for collision in player_collision_list:
            collision.on_collide(self.jugador)

        for proyectil in self.scene[CAPA_PROYECTIL]:
            proyectil_collision_list = arcade.check_for_collision_with_lists(
                proyectil,
                [
                    self.scene[CAPA_JUGADOR],
                    self.scene[CAPA_GOBLIN],
                    self.scene[CAPA_LUCIAN]
                ]
            )

            for collision in proyectil_collision_list:
                proyectil.on_collide(collision)

        player_collision_list = arcade.check_for_collision_with_lists(
            self.jugador,
            [
                self.scene[CAPA_LLAVE]
            ]
        )

        for collision in player_collision_list:
            collision.visible = False
            collision.center_x = -10000
            collision.center_y = -10000
            self.jugador.has_llave = True

        player_collision_list = arcade.check_for_collision_with_lists(
            self.jugador,
            [
                self.scene[CAPA_SALIDA]
            ]
        )
        for collision in player_collision_list:
            if isinstance(collision, PuertaSalida):
                collision.on_collide(self.jugador)

        self.camera.position = self.jugador.position
        self.camera.on_update()
        self.interfaz.update(delta_time)

    def on_draw(self):
        self.clear()

        with self.camera.activate():
            self.scene.draw(pixelated=True)

        self.interfaz.draw()


class Minijuego(Nivel):
    def __new__(cls, map: Path) -> "Minijuego":
        return object.__new__(cls)

    def _append_objetos_evento(self, tilemap: Tilemap, scene: arcade.Scene):
        scene.add_sprite_list(CAPA_EMISOR)
        scene.add_sprite_list(CAPA_RECEPTOR)
        scene.add_sprite_list(CAPA_RECEPTOR_PUERTA_ABIERTA)

        layer_emisor = tilemap._layer(CAPA_EMISOR)
        altura = tilemap.dict["height"] * tilemap.dict["tileheight"]

        if layer_emisor is None:
            return

        for objeto in layer_emisor["objects"]:
            if objeto["type"] == "Boton":
                    palanca = Boton(color = random.choice(["amarillo", "azul", "rojo", "verde"]),
                                    interaccion_pulsar=self.cambiar_estado, 
                                    interaccion_soltar=self.cambiar_estado,
                                    scale=objeto["height"]/64, 
                                    center_x=objeto["x"] + objeto["width"]/2, 
                                    center_y=altura - objeto["y"] + objeto["height"]/2)
                    scene.add_sprite(CAPA_EMISOR, palanca)

    def setup(self, map: Path):
        super().setup(map)

        self.interfaz.color = arcade.color.WHITE
        self.camera.zoom = 0.5

        self.red_walls = self.scene.get_sprite_list("Rojo")
        self.blue_walls = self.scene.get_sprite_list("Azul")
        self.llave = arcade.Sprite(Path("assets") / "images" / "llave.png", scale=2)
        self.llave.center_x = 1770
        self.llave.center_y = 3670
        self.scene.add_sprite(CAPA_LLAVE, self.llave)
        self.modo_rojo = False
        self.cambiar_estado()
        self.paredes_activas = self.red_walls if self.modo_rojo else self.blue_walls
        self.physics_engine_llave = arcade.PhysicsEnginePlatformer(
            self.llave, 
            walls=self.paredes_activas, 
            gravity_constant=0.5
        )
        self.llave.change_y = -3

    def on_update(self, delta_time: float):
        super().on_update(delta_time)

        self.llave.center_x += self.llave.change_x
        self.llave.center_y += self.llave.change_y

        if self.llave.center_y < 0: 
            self.llave.center_x = 1770
            self.llave.center_y = 3670

        self.paredes_activas = self.red_walls if self.modo_rojo else self.blue_walls

        colisiones = arcade.check_for_collision_with_list(self.llave, self.paredes_activas)
        if colisiones:
            pared = colisiones[0]
            self.llave.center_x -= self.llave.change_x
            self.llave.center_y += 10
            if len(str(Path(pared.texture.file_path).name)) > 18 and str(Path(pared.texture.file_path).name)[18] == 'd': self.llave.center_x += 20
            elif len(str(Path(pared.texture.file_path).name)) > 18 and str(Path(pared.texture.file_path).name)[18] == 'i': self.llave.center_x -= 20
            elif len(str(Path(pared.texture.file_path).name)) > 12 and str(Path(pared.texture.file_path).name)[12: 18] == "pincho": 
                self.llave.center_x = 1770
                self.llave.center_y = 3670
            elif len(str(Path(pared.texture.file_path).name)) > 12 and str(Path(pared.texture.file_path).name)[12: 22] == "plataforma": 
                self.llave.center_x = 5000
                self.llave.center_y = 5000
                self.llave.change_y = 0
                self.llave.change_x = 0
                self.llave.visible = False
                llave_final = Llave(2, 2142, 400)
                self.scene.add_sprite("Llave_final", llave_final)
            self.llave.center_x += self.llave.change_x

        if "Llave_final" in self.scene:
            player_collision_list = arcade.check_for_collision_with_lists(
                self.jugador,
                [
                    self.scene["Llave_final"]
                ]
            )
            for collision in player_collision_list:
                if self.scene["Llave_final"] in collision.sprite_lists:
                    print(collision)
                    collision.visible = False
                    collision.center_x = -10000
                    collision.center_y = -10000
                    self.jugador.has_llave = True

    def cambiar_estado(self):
        self.modo_rojo = not self.modo_rojo
        if self.modo_rojo:
            self.red_walls.visible = True
            self.blue_walls.visible = False
        else:
            self.red_walls.visible = False
            self.blue_walls.visible = True

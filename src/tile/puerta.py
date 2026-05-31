from pathlib import Path

import arcade
from entidad.jugador import Jugador
import config.controles as controles
from util import globales
from util import io


class Puerta(arcade.Sprite):
    _PATH_CERRADA: Path = Path("assets") / "images" / "puerta_cerrada.png"
    _PATH_ABIERTA: Path = Path("assets") / "images" / "puerta_abierta.png"

    def __init__(self, capa_receptor: arcade.SpriteList, capa_receptor_puerta_abierta: arcade.SpriteList, scale: float, center_x: float = 0, center_y: float = 0, angle: float = 0, abierta: bool = False, name: str = ""):
        super().__init__(self._PATH_CERRADA, scale, center_x, center_y, angle)

        self.capa_receptor = capa_receptor
        self.capa_receptor_puerta_abierta = capa_receptor_puerta_abierta
        self.name = name

        textura_abierta = arcade.texture.default_texture_cache.load_or_get_texture(self._PATH_ABIERTA)
        self.append_texture(textura_abierta)

        self._abierta: bool
        self._cambiar_textura(abierta)

    def _cambiar_textura(self, abierta: bool) -> None:
        self._abierta = abierta
        self.set_texture(int(self._abierta))

    def abrir(self) -> None:
        self.capa_receptor.remove(self)
        self.capa_receptor_puerta_abierta.append(self)
        self._cambiar_textura(True)

    def cerrar(self) -> None:
        self.capa_receptor.append(self)
        self.capa_receptor_puerta_abierta.remove(self)
        self._cambiar_textura(False)


class PuertaGris(arcade.Sprite):
    _PATH: Path = Path("assets") / "images" / "puerta_gris.png"
    def __init__(self, change: float, scale: float, center_x: float = 0, center_y: float = 0, angle: float = 0, abierta: bool = False, name: str = ""):
        super().__init__(self._PATH, scale, center_x, center_y, angle)
        self.change = change
        self.name = name
        self.abierta = abierta

    def abrir(self) -> None:
        self.angle += self.change
        self.change *= -1
    
    def cerrar(self) -> None:
        self.angle += self.change
        self.change *= -1

class PuertaNegra(arcade.Sprite):
    _PATH: Path = Path("assets") / "images" / "puerta_negra.png"
    def __init__(self, scale: float, center_x: float = 0, center_y: float = 0, angle: float = 0, abierta: bool = False, name: str = ""):
        super().__init__(self._PATH, scale, center_x, center_y, angle)
        self.name = name
        self.abierta = abierta
        self.posx = center_x
        self.posy = center_y

    def abrir(self) -> None:
        self.visible = False
        self.center_x = -1000
        self.center_y = -1000
    
    def cerrar(self) -> None:
        self.visible = True
        self.center_x = self.posx
        self.center_y = self.posy

class Llave(arcade.Sprite):
    _PATH: Path = Path("assets") / "images" / "llave.png"
    def __init__(self, scale: float, center_x: float = 0, center_y: float = 0, angle: float = 0, name: str = ""):
        super().__init__(self._PATH, scale, center_x, center_y, angle)
        self.name = name
        self.posx = center_x
        self.posy = center_y

class PuertaSalida(arcade.Sprite):
    _PATH: Path = Path("assets") / "images" / "puerta_cerrada_fondo.png"
    _PATH2: Path = Path("assets") / "images" / "puerta_abierta_fondo.png"
    def __init__(self, siguiente_nivel: Path, scale: float, center_x: float = 0, center_y: float = 0, angle: float = 0, name: str = ""):
        super().__init__(self._PATH, scale, center_x, center_y, angle)

        self.siguiente_nivel = siguiente_nivel

        self.name = name
        self.posx = center_x
        self.posy = center_y

        textura2 = arcade.texture.default_texture_cache.load_or_get_texture(self._PATH2)
        self.append_texture(textura2)

    def on_collide(self, entidad: arcade.Sprite) -> None:
        if not isinstance(entidad, Jugador):
            return

        if io.tecla_justo_pulsada(controles.palanca_interactuar):
            if(entidad._has_llave):
                from util.nivelazo import Nivel
                self.set_texture(1)
                globales.nivel.window.show_view(Nivel(self.siguiente_nivel))
            else:
                from util import globales
                globales.nivel.interfaz.mostrar_advertencia("¡Necesitas la llave para salir!")

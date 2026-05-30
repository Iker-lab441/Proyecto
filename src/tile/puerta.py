from pathlib import Path

import arcade


class Puerta(arcade.Sprite):
    _PATH_CERRADA: Path = Path("assets") / "images" / "puerta_cerrada.png"
    _PATH_ABIERTA: Path = Path("assets") / "images" / "puerta_abierta.png"

    def __init__(self, scale: float, center_x: float = 0, center_y: float = 0, angle: float = 0, abierta: bool = False, name: str = ""):
        super().__init__(self._PATH_CERRADA, scale, center_x, center_y, angle)
        self.name = name

        textura_abierta = arcade.texture.default_texture_cache.load_or_get_texture(self._PATH_ABIERTA)
        self.append_texture(textura_abierta)

        self._abierta: bool
        self._cambiar_textura(abierta)

    def _cambiar_textura(self, abierta: bool) -> None:
        self._abierta = abierta
        self.set_texture(int(self._abierta))

    def abrir(self) -> None:
        self._cambiar_textura(True)

    def cerrar(self) -> None:
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
        self.change *= (-1)
    
    def cerrar(self) -> None:
        self.angle += self.change
        self.change *= (-1)

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
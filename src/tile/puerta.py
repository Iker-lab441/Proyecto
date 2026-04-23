import arcade


class Puerta(arcade.Sprite):
    def __init__(self, textura_cerrada: str, textura_abierta: str, center_x = 0, center_y = 0, angle = 0, **kwargs):
        super().__init__(center_x, center_y, angle, **kwargs)

        textura_cerrada: str = arcade.texture.default_texture_cache.load_or_get_texture(textura_cerrada)
        textura_abierta: str = arcade.texture.default_texture_cache.load_or_get_texture(textura_abierta)

        self.texturas: dict[bool, arcade.Texture] = {
            False: textura_cerrada,
            True: textura_abierta
        }

        self._abierta: bool = False
        self._cambiar_textura(False)

    def _cambiar_textura(self, abierta: bool) -> None:
        self._abierta = abierta
        self.texture = self.TEXTURAS[self._abierta]

    def abrir(self) -> None:
        self._cambiar_textura(True)

    def cerrar(self) -> None:
        self._cambiar_textura(False)
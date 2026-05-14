from pathlib import Path
import arcade

import util.io
import config.controles as controles


class Jugador(arcade.Sprite):
    _VELOCIDAD: float = 400.0
    _HP: int = 3
    _SPRITE_SHEET_PATH: Path = Path("assets") / "player" / "thorneAndandoMejorado.png"

    def __init__(self, center_x: float, center_y: float) -> None:
        sprite_sheet = arcade.SpriteSheet(self._SPRITE_SHEET_PATH)
        textures = sprite_sheet.get_texture_grid((64, 64), 7, 7)

        super().__init__(textures[0], 1, center_x, center_y)
        self.textures = textures

        self._hp: int = self._HP
        self._muerto: bool = False

    def update(self, delta_time: float) -> None:
        super().update(delta_time)

        change_x: int = self.change_x

        self.change_x = 0

        if util.io.tecla_mantenida(controles.jugador_izquierda):
            self.change_x -= self._VELOCIDAD * delta_time

        if util.io.tecla_mantenida(controles.jugador_derecha):
            self.change_x += self._VELOCIDAD * delta_time

        # Si ha cambiado el signo
        if self.change_x * change_x <= 0:
            self.cur_texture = 0
            if self.change_x != 0:
                self.scale_x = util.signo(self.change_x) * abs(self.scale_x)
        else:
            self.cur_texture = (self.cur_texture + 1) % (len(self.textures) * 10)

        self.texture = self.textures[self.cur_texture // 10]

    def dañar(self) -> None:
        self._hp -= 1
        if self._hp == 0:
            self._muerto = True

    @property
    def esta_muerto(self) -> bool:
        return self._muerto
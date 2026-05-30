import arcade.gui as gui
import arcade
from pathlib import Path
import util.io
import config.controles as controles
from tile.nivel import Nivel


class Juego(arcade.View):
    def __init__(self):
        super().__init__()

    def on_update(self, delta_time: float) -> bool | None:
        if util.io.tecla_justo_pulsada(arcade.key.ESCAPE):
            from menu.menu_principal import MenuPrincipal # import local para evitar import circular
            self.window.show_view(MenuPrincipal())
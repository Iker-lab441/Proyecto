import arcade.gui as gui
import arcade
from pathlib import Path
import util.io
import config.controles as controles
#from tile.nivel import Nivel
from util.nivel import Tilemap, Nivel


class MenuDebug(gui.UIView):
    def __init__(self):
        super().__init__()

        titulo = gui.UILabel("THE TEST\n", width=400, height=100, font_size=20, multiline=True)
        boton_test_objeto_evento = gui.UIFlatButton(text="TESTEAR OBJETOS DE EVENTO", width=400, height=100)

        @boton_test_objeto_evento.event("on_click")
        def on_click(event: gui.UIOnClickEvent):
            """tilemap = Tilemap(Path("assets") / "maps" / "Mapa_prueba.json")
            print(tilemap._layer("Muros"))
            nivel = Nivel(Path("assets") / "maps" / "Mapa_prueba.json")
            #nivel = Nivel("Mapa_prueba4")
            self.window.show_view(nivel)"""
            tilemap = Tilemap(Path("assets") / "maps" / "prueba_laberinto.json")
            print(tilemap._layer("Jugador"))
            #print(tilemap._layer("Muros"))
            nivel = Nivel(tilemap)
            #print(nivel.__str__)
            #print(nivel.tilemap._layer("Bloques"))
            #print(nivel.scene.get_sprite_list("Muros").__dict__)
            self.window.show_view(nivel)


        box_layout = gui.UIBoxLayout(
            space_between=10,
            children=[titulo, boton_test_objeto_evento]
        )

        anchor_layout = gui.UIAnchorLayout(children=[box_layout], anchor_x="center_x", anchor_y="center_y")

        self.add_widget(anchor_layout)

    def on_update(self, delta_time: float) -> bool | None:
        if util.io.tecla_justo_pulsada(controles.menu_debug):
            from menu.menu_principal import MenuPrincipal # import local para evitar import circular
            self.window.show_view(MenuPrincipal())
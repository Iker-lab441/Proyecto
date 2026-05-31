import arcade.gui as gui
import arcade
from pathlib import Path
import util.io
import config.controles as controles
#from tile.nivel import Nivel
import util.nivel
import util.nivelazo


class MenuDebug(gui.UIView):
    def __init__(self):
        super().__init__()

        titulo = gui.UILabel("THE TEST\n", width=400, height=100, font_size=20, multiline=True)
        boton_test_objeto_evento = gui.UIFlatButton(text="TESTEAR OBJETOS DE EVENTO", width=400, height=100)
        boton_test_salto_pared = gui.UIFlatButton(text="TESTEAR SALTO DE PARED", width=400, height=100)
        boton_test_nivel_final = gui.UIFlatButton(text="TESTEAR NIVEL FINAL", width=400, height=100)
        boton_test_minijuego = gui.UIFlatButton(text="TESTEAR MINIJUEGO", width=400, height=100)
        boton_test_lucian = gui.UIFlatButton(text="TESTEAR LUCIAN", width=400, height=100)

        @boton_test_objeto_evento.event("on_click")
        def on_click_test_objeto_evento(event: gui.UIOnClickEvent):
            tilemap = util.nivel.Tilemap(Path("assets") / "maps" / "laberinto.json")
            nivel = util.nivel.Nivel(tilemap)
            self.window.show_view(nivel)

        @boton_test_salto_pared.event("on_click")
        def on_click_test_salto_pared(event: gui.UIOnClickEvent):
            nivel = util.nivelazo.Nivel(Path("assets") / "maps" / "test_salto_pared.json")
            self.window.show_view(nivel)

        @boton_test_nivel_final.event("on_click")
        def on_click_test_nivel_final(event: gui.UIOnClickEvent):
            nivel = util.nivelazo.Nivel(Path("assets") / "maps" / "nivel_final.json")
            self.window.show_view(nivel)

        @boton_test_minijuego.event("on_click")
        def on_click_test_parkour(event: gui.UIOnClickEvent):
            nivel = util.nivel.Minijuego(util.nivel.Tilemap(Path("assets") / "maps" / "minijuego.json"))
            self.window.show_view(nivel)

        @boton_test_lucian.event("on_click")
        def on_click_test_lucian(event: gui.UIOnClickEvent):
            nivel = util.nivelazo.Nivel(Path("assets") / "maps" / "jefe_final.json")
            self.window.show_view(nivel)

        box_layout = gui.UIBoxLayout(
            space_between=10,
            children=[titulo, boton_test_objeto_evento, boton_test_salto_pared, boton_test_nivel_final, boton_test_minijuego, boton_test_lucian]
        )

        anchor_layout = gui.UIAnchorLayout(children=[box_layout], anchor_x="center_x", anchor_y="center_y")
        self.add_widget(anchor_layout)

    def on_update(self, delta_time: float) -> bool | None:
        if util.io.tecla_justo_pulsada(controles.menu_debug):
            from menu.menu_principal import MenuPrincipal # import local para evitar import circular
            self.window.show_view(MenuPrincipal())
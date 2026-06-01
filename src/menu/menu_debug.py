import arcade.gui as gui
import arcade
from pathlib import Path
import util.io
import config.controles as controles
from util.nivel import Nivel


class MenuDebug(gui.UIView):
    def __init__(self):
        super().__init__()

        titulo = gui.UILabel("THE TEST\n", width=400, height=100, font_size=20, multiline=True)
        boton_test_laberinto = gui.UIFlatButton(text="TESTEAR LABERINTO", width=400, height=100)
        boton_test_parkour = gui.UIFlatButton(text="TESTEAR PARKOUR", width=400, height=100)
        boton_test_minijuego = gui.UIFlatButton(text="TESTEAR MINIJUEGO", width=400, height=100)
        boton_test_nivel_final = gui.UIFlatButton(text="TESTEAR NIVEL FINAL", width=400, height=100)
        boton_test_lucian = gui.UIFlatButton(text="TESTEAR LUCIAN", width=400, height=100)

        @boton_test_laberinto.event("on_click")
        def on_click_test_laberinto(event: gui.UIOnClickEvent):
            nivel = Nivel(Path("assets") / "maps" / "laberinto.json")
            self.window.show_view(nivel)

        @boton_test_parkour.event("on_click")
        def on_click_test_parkour(event: gui.UIOnClickEvent):
            nivel = Nivel(Path("assets") / "maps" / "parkour.json")
            self.window.show_view(nivel)

        @boton_test_minijuego.event("on_click")
        def on_click_test_minijuego(event: gui.UIOnClickEvent):
            nivel = Nivel(Path("assets") / "maps" / "minijuego.json")
            self.window.show_view(nivel)

        @boton_test_nivel_final.event("on_click")
        def on_click_test_nivel_final(event: gui.UIOnClickEvent):
            nivel = Nivel(Path("assets") / "maps" / "nivel_final.json")
            self.window.show_view(nivel)

        @boton_test_lucian.event("on_click")
        def on_click_test_lucian(event: gui.UIOnClickEvent):
            nivel = Nivel(Path("assets") / "maps" / "jefe_final.json")
            self.window.show_view(nivel)

        box_layout = gui.UIBoxLayout(
            space_between=10,
            children=[titulo, boton_test_laberinto, boton_test_parkour, boton_test_minijuego, boton_test_nivel_final, boton_test_lucian]
        )

        anchor_layout = gui.UIAnchorLayout(children=[box_layout], anchor_x="center_x", anchor_y="center_y")
        self.add_widget(anchor_layout)

    def on_update(self, delta_time: float) -> bool | None:
        if util.io.tecla_justo_pulsada(controles.menu_debug):
            from menu.menu_principal import MenuPrincipal # import local para evitar import circular
            self.window.show_view(MenuPrincipal())
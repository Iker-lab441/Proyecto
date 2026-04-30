import arcade.gui as gui

import util.io
import config.controles as controles


class MenuDebug(gui.UIView):
    def __init__(self):
        super().__init__()

        titulo = gui.UILabel("THE TEST\n", width=400, height=100, font_size=20, multiline=True)
        boton_test_objeto_evento = gui.UIFlatButton(text="TESTEAR OBJETOS DE EVENTO", width=400, height=100)

        @boton_test_objeto_evento.event("on_click")
        def on_click(event: gui.UIOnClickEvent):
            pass

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
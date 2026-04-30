import arcade.gui as gui

import util.io
import config.controles as controles


class MenuPrincipal(gui.UIView):
    def __init__(self):
        super().__init__()

        titulo = gui.UILabel("THE GAME\n", width=400, height=100, font_size=20, multiline=True)
        boton_nueva_partida = gui.UIFlatButton(text="NUEVA PARTIDA", width=400, height=100)
        boton_continuar = gui.UIFlatButton(text="CONTINUAR", width=400, height=100)
        boton_ayuda = gui.UIFlatButton(text="AYUDA", width=400, height=100)

        box_layout = gui.UIBoxLayout(
            space_between=10,
            children=[titulo, boton_nueva_partida, boton_continuar, boton_ayuda]
        )

        anchor_layout = gui.UIAnchorLayout(children=[box_layout], anchor_x="center_x", anchor_y="center_y")

        self.add_widget(anchor_layout)

    def on_update(self, delta_time: float) -> bool | None:
        if util.io.tecla_justo_pulsada(controles.menu_debug):
            from menu.menu_debug import MenuDebug # import local para evitar import circular
            self.window.show_view(MenuDebug())
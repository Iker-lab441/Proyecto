import arcade.gui as gui
import util.io
import config.controles as controles

def nombre_tecla(codigo: int) -> str:
    import pyglet.window.key as pkey
    nombre = pkey.symbol_string(codigo)
    traducciones = {
        "SPACE": "Espacio", "ENTER": "Enter", 
        "UP": "Arriba", "DOWN": "Abajo", 
        "LEFT": "Izquierda", "RIGHT": "Derecha"
    }
    return traducciones.get(nombre, nombre)

class MenuAsignacion(gui.UIView):
    def __init__(self) -> None:
        super().__init__()

        self.boton_esperando: gui.UIFlatButton | None = None
        self.tecla_esperando: int | None = None
        self.attr_tecla_esperando: str | None = None

        self.controles_lista: list[tuple[int, str, str]] = [
            (controles.jugador_izquierda, "jugador_izquierda", "Mover Izquierda"),
            (controles.jugador_derecha, "jugador_derecha", "Mover Derecha"),
            (controles.jugador_salto, "jugador_salto", "Saltar")
        ]

        anchor_layout = gui.UIAnchorLayout(anchor_x="center_x", anchor_y="center_y")
        self.add_widget(anchor_layout)

        box_layout = gui.UIBoxLayout(space_between=20)
        anchor_layout.add(box_layout)

        titulo = gui.UILabel(text="ASIGNACIÓN DE CONTROLES", width=400, height=50, font_size=20, bold=True, align="center")
        box_layout.add(titulo)

        caja_controles = gui.UIGridLayout(column_count=2, row_count=len(self.controles_lista), horizontal_spacing=20, vertical_spacing=20)
        box_layout.add(caja_controles)

        for n, (tecla, attr_tecla, descripcion) in enumerate(self.controles_lista):
            texto_boton = nombre_tecla(tecla)

            boton_tecla = gui.UIFlatButton(text=texto_boton, width=150, height=40)
            label_descripcion = gui.UILabel(text=descripcion, width=200, height=40, font_size=16)

            self.crear_evento_boton(boton_tecla, tecla, attr_tecla)

            caja_controles.add(boton_tecla, column=0, row=n)
            caja_controles.add(label_descripcion, column=1, row=n)

        self.texto_info: gui.UILabel = gui.UILabel(
            text="* Haz clic en un botón y presiona la nueva tecla.\n* Presiona ESC para cancelar.",
            width=400, height=50,
            font_size=12,
            multiline=True,
            align="center"
        )
        box_layout.add(self.texto_info)

        boton_volver = gui.UIFlatButton(text="VOLVER", width=400, height=50)

        @boton_volver.event("on_click")
        def on_click_volver(event):
            from menu.menu_ayuda import MenuAyuda
            self.window.show_view(MenuAyuda())

        box_layout.add(boton_volver)

    def crear_evento_boton(self, boton: gui.UIFlatButton, tecla: int, attr_tecla: str) -> None:
        @boton.event("on_click")
        def on_click(event):
            if self.boton_esperando and self.tecla_esperando and self.attr_tecla_esperando:
                self.boton_esperando.text = nombre_tecla(self.tecla_esperando)

            self.boton_esperando = boton
            self.tecla_esperando = tecla
            self.attr_tecla_esperando = attr_tecla
            boton.text = "-"

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.texto_info.text = "* Haz clic en un botón y presiona la nueva tecla.\n* Presiona ESC para cancelar."

        if self.boton_esperando and self.tecla_esperando and self.attr_tecla_esperando:
            if symbol == controles.cancelar_asignacion_de_boton:
                self.boton_esperando.text = nombre_tecla(self.tecla_esperando)
            else:
                tecla_en_uso = False
                for tecla, _, _ in self.controles_lista:
                    if tecla == symbol and tecla != self.tecla_esperando:
                        tecla_en_uso = True
                        break

                if tecla_en_uso:
                    self.texto_info.text = "¡ERROR: Tecla ya asignada!\nElige otra o pulsa ESC para cancelar."
                    self.boton_esperando.text = nombre_tecla(self.tecla_esperando)
                else:
                    setattr(controles, self.attr_tecla_esperando, symbol)
                    self.boton_esperando.text = nombre_tecla(symbol)

            self.boton_esperando = None
            self.tecla_esperando = None
            self.attr_tecla_esperando = None
            self.texto_info.fit_content()

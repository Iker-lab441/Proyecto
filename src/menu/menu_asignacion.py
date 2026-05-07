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
    def __init__(self):
        super().__init__()

        self.control_esperando = None 
        self.boton_esperando = None   

        titulo = gui.UILabel(text="ASIGNACIÓN DE CONTROLES", width=400, height=50, font_size=20, bold=True, align="center")
        
        self.box_layout = gui.UIBoxLayout(space_between=20)
        self.box_layout.add(titulo)

        self.controles_lista = [
            ("jugador_izquierda", "Mover Izquierda"),
            ("jugador_derecha", "Mover Derecha"),
            ("jugador_salto", "Saltar")
        ]

        for attr, desc in self.controles_lista:
            fila = gui.UIBoxLayout(vertical=False, space_between=20)
            
            valor_actual = getattr(controles, attr)
            texto_boton = nombre_tecla(valor_actual)
            
            boton = gui.UIFlatButton(text=texto_boton, width=150, height=40)
            label = gui.UILabel(text=desc, width=200, height=40, font_size=16)
            
            self.crear_evento_boton(boton, attr)
            
            fila.add(boton)
            fila.add(label)
            self.box_layout.add(fila)

        self.texto_info = gui.UILabel(
            text="* Haz clic en un botón y presiona la nueva tecla.\n* Presiona ESC para cancelar.",
            width=400, height=50,
            font_size=12,
            multiline=True,
            align="center"
        )
        self.box_layout.add(self.texto_info)

        boton_volver = gui.UIFlatButton(text="VOLVER", width=400, height=50)

        @boton_volver.event("on_click")
        def on_click_volver(event):
            from menu.menu_ayuda import MenuAyuda
            self.window.show_view(MenuAyuda())

        self.box_layout.add(boton_volver)

        anchor_layout = gui.UIAnchorLayout(children=[self.box_layout], anchor_x="center_x", anchor_y="center_y")
        self.add_widget(anchor_layout)

    def crear_evento_boton(self, boton, attr_name):
        @boton.event("on_click")
        def on_click(event):
            if self.boton_esperando and self.control_esperando:
                old_val = getattr(controles, self.control_esperando)
                self.boton_esperando.text = nombre_tecla(old_val)
                
            self.control_esperando = attr_name
            self.boton_esperando = boton
            boton.text = "-"

    def on_key_press(self, symbol: int, modifiers: int):
        import arcade.key as key
        
        self.texto_info.text = "* Haz clic en un botón y presiona la nueva tecla.\n* Presiona ESC para cancelar."
        
        if self.control_esperando:
            if symbol == key.ESCAPE:
                old_val = getattr(controles, self.control_esperando)
                self.boton_esperando.text = nombre_tecla(old_val)
            else:
                tecla_en_uso = False
                for attr, _ in self.controles_lista:
                    if getattr(controles, attr) == symbol and attr != self.control_esperando:
                        tecla_en_uso = True
                        break
                
                if tecla_en_uso:
                    self.texto_info.text = "¡ERROR: Tecla ya asignada!\nElige otra o pulsa ESC para cancelar."
                    old_val = getattr(controles, self.control_esperando)
                    self.boton_esperando.text = nombre_tecla(old_val)
                else:
                    setattr(controles, self.control_esperando, symbol)
                    self.boton_esperando.text = nombre_tecla(symbol)
            
            self.control_esperando = None
            self.boton_esperando = None
        else:
            pass 
        super().on_key_press(symbol, modifiers)

    def on_update(self, delta_time: float) -> bool | None:
        if util.io.tecla_justo_pulsada(controles.menu_debug):
            from menu.menu_principal import MenuPrincipal 
            self.window.show_view(MenuPrincipal())
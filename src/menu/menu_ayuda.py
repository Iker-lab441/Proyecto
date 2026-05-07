import arcade.gui as gui
import config.controles as controles

class MenuAyuda(gui.UIView):
    def __init__(self):
        super().__init__()

        titulo = gui.UILabel(
            text="PANTALLA DE AYUDA", 
            width=400, height=50, 
            font_size=24, 
            bold=True, 
            align="center"
        )

        def nombre_tecla(codigo: int) -> str:
            import pyglet.window.key as pkey
            nombre = pkey.symbol_string(codigo)
            traducciones = {
                "SPACE": "Espacio", "ENTER": "Enter", 
                "UP": "Arriba", "DOWN": "Abajo", 
                "LEFT": "Izquierda", "RIGHT": "Derecha"
            }
            return traducciones.get(nombre, nombre)

        str_izq = nombre_tecla(controles.jugador_izquierda).ljust(7)
        str_der = nombre_tecla(controles.jugador_derecha).ljust(7)
        str_salto = nombre_tecla(controles.jugador_salto).ljust(7)

        controles_texto = (
            f"CONTROLES DEL JUEGO\n"
            f"-----------------------------\n"
            f" {str_izq} :  Mover Izquierda\n"
            f" {str_der} :  Mover Derecha\n"
            f" {str_salto} :  Saltar"
        )
        
        texto_controles = gui.UILabel(
            text=controles_texto, 
            width=400, height=150, 
            font_size=16, 
            multiline=True,
            font_name="Courier"
        )
        
        boton_volver = gui.UIFlatButton(text="VOLVER", width=400, height=50)

        @boton_volver.event("on_click")
        def on_click_volver(event):
            from menu.menu_principal import MenuPrincipal
            self.window.show_view(MenuPrincipal())

        boton_asignacion = gui.UIFlatButton(text="ASIGNAR CONTROLES", width=400, height=50)
        @boton_asignacion.event("on_click")
        def on_click_asignacion(event):
            from menu.menu_asignacion import MenuAsignacion
            self.window.show_view(MenuAsignacion())

        box_layout = gui.UIBoxLayout(
            space_between=20,
            children=[titulo, texto_controles, boton_asignacion, boton_volver]
        )

        anchor_layout = gui.UIAnchorLayout(children=[box_layout], anchor_x="center_x", anchor_y="center_y")
        self.add_widget(anchor_layout)
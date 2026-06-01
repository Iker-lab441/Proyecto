import arcade
import arcade.gui as gui
import os
import config.controles as controles

def nombre_tecla(codigo: int) -> str:
    if codigo == arcade.MOUSE_BUTTON_LEFT: return "Clk Izq"
    if codigo == arcade.MOUSE_BUTTON_RIGHT: return "Clk Der"
    
    import pyglet.window.key as pkey
    nombre = pkey.symbol_string(codigo)
    traducciones = {
        "SPACE": "Espacio", "ENTER": "Enter", 
        "UP": "Arriba", "DOWN": "Abajo", 
        "LEFT": "Izquierda", "RIGHT": "Derecha"
    }
    return traducciones.get(nombre, nombre)

class MenuAsignacion(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.manager = gui.UIManager()
        self.manager.enable()

        ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        ruta_fondo = os.path.join(ruta_base, "assets", "images", "fondo_opciones.png")
        ruta_boton = os.path.join(ruta_base, "assets", "images", "boton_menu_principal.png")
        ruta_boton_hover = os.path.join(ruta_base, "assets", "images", "boton_menu_principal_hover.png")
        ruta_boton_pressed = os.path.join(ruta_base, "assets", "images", "boton_menu_principal_pressed.png")
        
       
        ruta_fuente = os.path.join(ruta_base, "assets", "fonts", "font_menu_principal.ttf")

        self.fondo_textura = arcade.load_texture(ruta_fondo)
        self.tex_madera = arcade.load_texture(ruta_boton)
        self.tex_madera_hover = arcade.load_texture(ruta_boton_hover)
        self.tex_madera_pressed = arcade.load_texture(ruta_boton_pressed)
        
       
        try:
            arcade.load_font(ruta_fuente)
            self.nombre_fuente = "Deutsch Gothic"
        except FileNotFoundError:
            self.nombre_fuente = "Arial"

        dorado_menu = (255, 203, 16)

        
        self.boton_esperando = None
        self.attr_tecla_esperando: str | None = None
        self.desc_esperando: str | None = None 

        self.controles_lista: list[tuple[str, str]] = [
            ("jugador_izquierda", "Mover Izquierda"),
            ("jugador_derecha", "Mover Derecha"),
            ("jugador_abajo", "Bajar"),
            ("jugador_salto", "Saltar"),
            ("palanca_interactuar", "Interactuar"),
            ("boton_disparar", "Disparar")
        ]

        estilo_boton = {
            "normal": {"font_size": 18, "font_name": self.nombre_fuente, "font_color": arcade.color.WHITE},
            "hover": {"font_size": 18, "font_name": self.nombre_fuente, "font_color": dorado_menu},
            "press": {"font_size": 18, "font_name": self.nombre_fuente, "font_color": arcade.color.LIGHT_GRAY}
        }

        box_layout = gui.UIBoxLayout(space_between=20)

        titulo = gui.UILabel(
            text="ASIGNACIÓN DE CONTROLES\n", 
            width=600, height=80, 
            font_size=45, 
            font_name=self.nombre_fuente,
            text_color=arcade.color.GOLDENROD, 
            align="center"
        )
        box_layout.add(titulo)

        
        for attr_tecla, descripcion in self.controles_lista:
            codigo_actual = getattr(controles, attr_tecla)
            tecla_str = nombre_tecla(codigo_actual).ljust(7)
            texto_boton = f"{tecla_str} :  {descripcion}"

            boton_control = gui.UITextureButton(
                texture=self.tex_madera,
                texture_hovered=self.tex_madera_hover,
                texture_pressed=self.tex_madera_pressed,
                text=texto_boton,
                width=400, height=50,
                style=estilo_boton
            )

            self.crear_evento_boton(boton_control, attr_tecla, descripcion)
            box_layout.add(boton_control)

        self.texto_info: gui.UILabel = gui.UILabel(
            text="* Haz clic en un botón y presiona la nueva tecla.\n* Presiona ESC para cancelar.",
            width=600, height=50,
            font_size=16,
            multiline=True,
            font_name=self.nombre_fuente,
            text_color=arcade.color.WHITE,
            align="center"
        )
        box_layout.add(self.texto_info)

        boton_volver = gui.UITextureButton(
            texture=self.tex_madera,
            texture_hovered=self.tex_madera_hover,
            texture_pressed=self.tex_madera_pressed,
            text="VOLVER", 
            width=400, height=50,
            style=estilo_boton
        )

        @boton_volver.event("on_click")
        def on_click_volver(event: gui.UIOnClickEvent):
            from menu.menu_ayuda import MenuAyuda
            self.manager.disable()
            self.window.show_view(MenuAyuda())

        box_layout.add(boton_volver)

        self.anchor_layout = gui.UIAnchorLayout()
        self.anchor_layout.add(child=box_layout, anchor_x="center_x", anchor_y="center_y", align_y=-20)
        self.manager.add(self.anchor_layout)

    def crear_evento_boton(self, boton, attr_tecla: str, descripcion: str) -> None:
        @boton.event("on_click")
        def on_click(event: gui.UIOnClickEvent):
            if self.boton_esperando and self.attr_tecla_esperando:
                tecla_antigua = getattr(controles, self.attr_tecla_esperando)
                tecla_str = nombre_tecla(tecla_antigua).ljust(7)
                self.boton_esperando.text = f"{tecla_str} :  {self.desc_esperando}"

            self.boton_esperando = boton
            self.attr_tecla_esperando = attr_tecla
            self.desc_esperando = descripcion
            boton.text = f"-       :  {descripcion}"

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.texto_info.text = "* Haz clic en un botón y presiona la nueva tecla.\n* Presiona ESC para cancelar."

        if self.boton_esperando and self.attr_tecla_esperando:
            if symbol == controles.escape:
                tecla_orig = getattr(controles, self.attr_tecla_esperando)
                tecla_str = nombre_tecla(tecla_orig).ljust(7)
                self.boton_esperando.text = f"{tecla_str} :  {self.desc_esperando}"
            else:
                tecla_en_uso = False
                for attr_name, _ in self.controles_lista:
                    if getattr(controles, attr_name) == symbol and attr_name != self.attr_tecla_esperando:
                        tecla_en_uso = True
                        break

                if tecla_en_uso:
                    self.texto_info.text = "¡ERROR: Tecla ya asignada!\nElige otra o pulsa ESC para cancelar."
                    tecla_orig = getattr(controles, self.attr_tecla_esperando)
                    tecla_str = nombre_tecla(tecla_orig).ljust(7)
                    self.boton_esperando.text = f"{tecla_str} :  {self.desc_esperando}"
                else:
                    setattr(controles, self.attr_tecla_esperando, symbol)
                    tecla_str = nombre_tecla(symbol).ljust(7)
                    self.boton_esperando.text = f"{tecla_str} :  {self.desc_esperando}"

            self.boton_esperando = None
            self.attr_tecla_esperando = None
            self.desc_esperando = None

    def on_draw(self):
        self.clear()
        
        ancho = 1280
        alto = 720
        if self.window:
            ancho = self.window.width
            alto = self.window.height

        if hasattr(self, 'fondo_textura'):
            arcade.draw_texture_rect(self.fondo_textura, arcade.LBWH(0, 0, ancho, alto))
            
        self.manager.draw()

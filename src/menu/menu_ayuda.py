import arcade
import arcade.gui as gui
import os
import traceback
import config.controles as controles

class MenuAyuda(arcade.View):
    def __init__(self):
        super().__init__()
        
        self.manager = gui.UIManager()
        self.manager.enable()

        # 1. Rutas de archivos
        ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        ruta_fondo = os.path.join(ruta_base, "assets", "images", "fondo_opciones.png")
        ruta_boton = os.path.join(ruta_base, "assets", "images", "boton_menu_principal.png")
        ruta_boton_hover = os.path.join(ruta_base, "assets", "images", "boton_menu_principal_hover.png")
        ruta_boton_pressed = os.path.join(ruta_base, "assets", "images", "boton_menu_principal_pressed.png")
        ruta_fuente = os.path.join(ruta_base, "assets", "fonts", "font_menu_principal.ttf")

        # 2. Carga de texturas
        self.fondo_textura = arcade.load_texture(ruta_fondo)
        self.tex_madera = arcade.load_texture(ruta_boton)
        self.tex_madera_hover = arcade.load_texture(ruta_boton_hover)
        self.tex_madera_pressed = arcade.load_texture(ruta_boton_pressed)
        
        # 3. Carga segura de la fuente (Este try sí es bueno dejarlo)
        try:
            arcade.load_font(ruta_fuente)
            self.nombre_fuente = "Deutsch Gothic"
        except FileNotFoundError:
            self.nombre_fuente = "Arial"

        dorado_menu = (255, 203, 16)

        # 4. Creación de la Interfaz
        titulo = gui.UILabel(
            text="PANTALLA DE AYUDA\n", 
            width=600, height=100, 
            font_size=50, 
            multiline=True,
            font_name=self.nombre_fuente, 
            text_color=arcade.color.GOLDENROD, 
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
            font_size=20,
            multiline=True,
            font_name=self.nombre_fuente,
            text_color=arcade.color.WHITE,
            align="left"
        )

        estilo_boton = {
            "normal": {
                "font_size": 18,
                "font_name": self.nombre_fuente,
                "font_color": arcade.color.WHITE
            },
            "hover": {
                "font_size": 18,
                "font_name": self.nombre_fuente,
                "font_color": dorado_menu
            },
            "press": {
                "font_size": 18,
                "font_name": self.nombre_fuente,
                "font_color": arcade.color.LIGHT_GRAY
            }
        }

        boton_asignacion = gui.UITextureButton(
            texture=self.tex_madera,
            texture_hovered=self.tex_madera_hover,
            texture_pressed=self.tex_madera_pressed,
            text="ASIGNAR CONTROLES",
            width=320, height=60,
            style=estilo_boton
        )
        
        @boton_asignacion.event("on_click")
        def on_click_asignacion(event):
            from menu.menu_asignacion import MenuAsignacion
            self.manager.disable()
            self.window.show_view(MenuAsignacion())
        
        boton_volver = gui.UITextureButton(
            texture=self.tex_madera,
            texture_hovered=self.tex_madera_hover,
            texture_pressed=self.tex_madera_pressed,
            text="VOLVER",
            width=320, height=60,
            style=estilo_boton
        )

        @boton_volver.event("on_click")
        def on_click_volver(event):
            from menu.menu_principal import MenuPrincipal
            self.manager.disable()
            self.window.show_view(MenuPrincipal())

        box_layout = gui.UIBoxLayout(
            space_between=20,
            children=[titulo, texto_controles, boton_asignacion, boton_volver]
        )

        self.anchor_layout = gui.UIAnchorLayout()
        self.anchor_layout.add(
            child=box_layout,
            anchor_x="center_x",
            anchor_y="center_y"
        )
        
        self.manager.add(self.anchor_layout)

    def on_draw(self):
        self.clear()
        
        ancho = 1280
        alto = 720
        if self.window:
            ancho = self.window.width
            alto = self.window.height

        # Solo dibujamos el fondo si se cargó correctamente
        if hasattr(self, 'fondo_textura'):
            arcade.draw_texture_rect(self.fondo_textura, arcade.LBWH(0, 0, ancho, alto))
        
        self.manager.draw()
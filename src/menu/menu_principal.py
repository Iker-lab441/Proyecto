import arcade
import arcade.gui as gui
import os
import util.io
from util import globales
import config.controles as controles

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
class MenuPrincipal(arcade.View):
    def __init__(self):
        super().__init__()
        ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        ruta_fondo = os.path.join(ruta_base, "assets", "images", "fondo_principal.png")
        
        self.fondo = arcade.load_texture(ruta_fondo)

        self.manager = gui.UIManager()
        self.manager.enable()

        ruta_boton = os.path.join(ruta_base, "assets", "images", "boton_menu_principal.png")
        ruta_boton_hover = os.path.join(ruta_base, "assets", "images", "boton_menu_principal_hover.png")
        ruta_boton_pressed = os.path.join(ruta_base, "assets", "images", "boton_menu_principal_pressed.png")
        self.textura_boton = arcade.load_texture(ruta_boton)
        self.textura_boton_hover = arcade.load_texture(ruta_boton_hover)
        self.textura_boton_pressed = arcade.load_texture(ruta_boton_pressed)

        ruta_fuente = os.path.join(ruta_base, "assets", "fonts", "font_menu_principal.ttf")
        arcade.load_font(ruta_fuente)

        # Musica
        globales.audio.reproducir_musica("musica_menu")
        titulo = gui.UILabel("THE GAME\n", width=600, height=120, font_size=65, multiline=True, font_name="Deutsch Gothic",text_color=arcade.color.GOLDENROD, align ="center")

        # Estilo para el texto de los botones
        dorado_menu = (255, 203, 16)
        estilo_boton = {
            "normal": {
                "font_size": 18,
                "font_name": "Deutsch Gothic",
                "font_color": arcade.color.WHITE
            },
            "hover": {
                "font_size": 18,
                "font_name": "Deutsch Gothic",
                "font_color": dorado_menu
            },
            "press": {
                "font_size": 18,
                "font_name": "Deutsch Gothic",
                "font_color": arcade.color.LIGHT_GRAY
            }
        }

        # Boton nueva partida
        boton_nueva_partida = gui.UITextureButton(
        texture = self.textura_boton, texture_hovered=self.textura_boton_hover,
        texture_pressed=self.textura_boton_pressed,
        text = "NUEVA PARTIDA", width = 320, height = 60, style=estilo_boton)

        # Boton continuar
        boton_continuar = gui.UITextureButton(
        texture = self.textura_boton, texture_hovered=self.textura_boton_hover,
        texture_pressed=self.textura_boton_pressed,
        text = "CONTINUAR", width = 320, height = 60, style = estilo_boton)

        # Boton opciones
        boton_opciones = gui.UITextureButton(
        texture = self.textura_boton, texture_hovered=self.textura_boton_hover,
        texture_pressed=self.textura_boton_pressed,
        text = "OPCIONES", width = 320, height = 60, style = estilo_boton)

        # Boton creditos
        boton_creditos = gui.UITextureButton(
        texture = self.textura_boton, texture_hovered=self.textura_boton_hover,
        texture_pressed=self.textura_boton_pressed,
        text="CRÉDITOS", width = 320, height = 60, style = estilo_boton)

        # Boton salir
        boton_salir = gui.UITextureButton(
        texture = self.textura_boton,texture_hovered=self.textura_boton_hover,
        texture_pressed=self.textura_boton_pressed,
        text = "SALIR", width = 320, height = 60, style = estilo_boton)

        @boton_opciones.event("on_click")
        def on_click_opciones(event):
            from menu.menu_ayuda import MenuAyuda
            self.manager.disable() 
            self.window.show_view(MenuAyuda())
        
        @boton_salir.event("on_click")
        def on_click_salir(event):
            arcade.exit()

        box_layout = gui.UIBoxLayout(
            space_between = 8,
            children=[titulo, boton_nueva_partida, boton_continuar, boton_opciones, boton_creditos, boton_salir]
        )
        
        self.anchor_layout = gui.UIAnchorLayout()

        self.anchor_layout.add(
            child=box_layout,
            anchor_x="center_x",
            anchor_y="center_y",
            align_y= -60
        )

        self.manager.add(self.anchor_layout)
    
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.fondo, arcade.LBWH(0, 0, self.window.width, self.window.height))
        self.manager.draw()

    def on_update(self, delta_time: float) -> bool | None:
        if util.io.tecla_justo_pulsada(controles.menu_debug):
            from menu.menu_debug import MenuDebug 
            self.manager.disable()
            self.window.show_view(MenuDebug())
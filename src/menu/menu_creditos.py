import arcade
import arcade.gui as gui
import os


class MenuCreditos(arcade.View):
    def __init__(self):
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

        
        titulo = gui.UILabel(
            text="CRÉDITOS\n",
            width=600, height=100,
            font_size=50,
            multiline=True,
            font_name=self.nombre_fuente,
            text_color=arcade.color.GOLDENROD,
            align="center"
        )

        equipo_texto = (
            "EQUIPO DE DESARROLLO\n"
            "-----------------------------------------------------------\n"
            "  Iker          —   Jefe y mecánicas\n"
            "  Mario        —   Menús y audio\n"
            "  Izan           —   Arte y sprites\n"
            "  Carlos       —   Mapas y mecánicas\n"
            "  Kevin         —   Historia y narrativa\n"
        )

        texto_equipo = gui.UILabel(
            text=equipo_texto,
            width=500, height=220,
            font_size=18,
            multiline=True,
            font_name=self.nombre_fuente,
            text_color=arcade.color.WHITE,
            align="left"
        )

        agradecimientos_texto = (
            "AGRADECIMIENTOS\n"
            "-----------------------------------------------------------\n"
            "  A nuestro profesor, por su guía\n"
            "  durante el desarrollo del proyecto.\n"
        )

        texto_agradecimientos = gui.UILabel(
            text=agradecimientos_texto,
            width=500, height=120,
            font_size=18,
            multiline=True,
            font_name=self.nombre_fuente,
            text_color=arcade.color.LIGHT_GRAY,
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
            children=[titulo, texto_equipo, texto_agradecimientos, boton_volver]
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

        ancho = self.window.width if self.window else 1280
        alto = self.window.height if self.window else 720

        if hasattr(self, 'fondo_textura'):
            arcade.draw_texture_rect(self.fondo_textura, arcade.LBWH(0, 0, ancho, alto))

        self.manager.draw()
import arcade
import arcade.gui as gui
import sys
import os
import util.io
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
        self.textura_boton = arcade.load_texture(ruta_boton)

        titulo = gui.UILabel("THE GAME\n", width=400, height=100, font_size=30, multiline=True,text_color=arcade.color.WHITE, align ="center")

        # Boton nueva partida
        boton_nueva_partida = gui.UITextureButton(
        texture = self.textura_boton, texture_hovered = self.textura_boton, 
        texture_pressed = self.textura_boton,
        text = "NUEVA PARTIDA", width = 320, height = 60)

        # Boton continuar
        boton_continuar = gui.UITextureButton(
        texture = self.textura_boton, texture_hovered = self.textura_boton,
        texture_pressed = self.textura_boton,
        text = "CONTINUAR", width = 320, height = 60)

        # Boton opciones
        boton_opciones = gui.UITextureButton(
        texture = self.textura_boton, texture_hovered = self.textura_boton,
        texture_pressed = self.textura_boton,
        text = "OPCIONES", width = 320, height = 60)

        # Boton creditos
        boton_creditos = gui.UITextureButton(
        texture = self.textura_boton, texture_hovered = self.textura_boton, 
        texture_pressed = self.textura_boton,
        text="CRÉDITOS", width = 320, height = 60)

        # Boton salir
        boton_salir = gui.UITextureButton(
            texture = self.textura_boton, texture_hovered = self.textura_boton,
            texture_pressed = self.textura_boton,
            text = "SALIR", width = 320, height = 60)

        @boton_opciones.event("on_click")
        def on_click_opciones(event):
            from menu.menu_ayuda import MenuAyuda
            self.manager.disable() 
            self.window.show_view(MenuAyuda())
        
        @boton_salir.event("on_click")
        def on_click_salir(event):
            arcade.exit()

        box_layout = gui.UIBoxLayout(
            space_between = 5,
            children=[titulo, boton_nueva_partida, boton_continuar, boton_opciones, boton_creditos, boton_salir]
        )
        
        # Usamos UIAnchorLayout, que es el que reconoce tu versión de Arcade
        self.anchor_layout = gui.UIAnchorLayout()

        # Añadimos el box_layout dentro del anchor_layout
        # Es AQUÍ donde definimos el anclaje y el desplazamiento
        self.anchor_layout.add(
            child=box_layout,
            anchor_x="center_x",
            anchor_y="center_y",
            align_y= -80  # Este número es el que empuja todo hacia abajo
        )

        # Finalmente, añadimos el layout principal al manager
        self.manager.add(self.anchor_layout)
    
    def on_draw(self):
        self.clear()
        # Dibujamos el fondo
        arcade.draw_texture_rect(self.fondo, arcade.LBWH(0, 0, self.window.width, self.window.height))
        #Dibujamos la interfaz por encima
        self.manager.draw()

    def on_update(self, delta_time: float) -> bool | None:
        if util.io.tecla_justo_pulsada(controles.menu_debug):
            from menu.menu_debug import MenuDebug # import local para evitar import circular
            self.manager.disable() # Desactivamos el UI actual
            self.window.show_view(MenuDebug())
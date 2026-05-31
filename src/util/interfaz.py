import arcade

class InterfazNivel:
    def __init__(self, window_width: int, window_height: int):
        self.width = window_width
        self.height = window_height
        
        # Textos a mostrar (vacío = no se muestra nada)
        self.texto_dialogo: str = ""
        self.texto_advertencia: str = ""
        
        # Cámara exclusiva de la UI (fija a la ventana, no afectada por el mapa)
        self.camara_ui = arcade.Camera2D()

    def dibujar(self):
        # Activar la cámara de la interfaz para dibujar sobre la pantalla, no sobre el mapa
        self.camara_ui.use()
        
        # Diálogos (Parte superior)
        if self.texto_dialogo:
            arcade.draw_text(
                self.texto_dialogo,
                self.width / 2,
                self.height - 50,
                arcade.color.WHITE,
                font_size=24,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )
            
        # Advertencias de puertas, etc (Cuarto inferior de la pantalla)
        if self.texto_advertencia:
            arcade.draw_text(
                self.texto_advertencia,
                self.width / 2,
                self.height * 0.25,
                arcade.color.RED,
                font_size=20,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

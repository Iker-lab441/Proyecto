import arcade
import arcade.gui

from util import globales, texturas

class InterfazNivel:
    def __init__(self, window_width: int, window_height: int):
        self.width = window_width
        self.height = window_height

        # Textos a mostrar (vacío = no se muestra nada)
        self.texto_dialogo: str = ""
        self.texto_advertencia: str = ""
        self.tiempo_advertencia: float = 0.0

        # Cámara exclusiva de la UI (fija a la ventana, no afectada por el mapa)
        self.camara_ui = arcade.Camera2D()

        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        self.caja_corazones = arcade.gui.UIBoxLayout(vertical=False, space_between=5)

        self.ui_manager.add(
            arcade.gui.UIAnchorLayout(
                anchor_x='left',
                anchor_y='top',
                align_x=20,
                align_y=-20,
                children=[self.caja_corazones]
            )
        )

    def mostrar_advertencia(self, texto: str, duracion: float = 3.0):
        self.texto_advertencia = texto
        self.tiempo_advertencia = duracion

    def update(self, delta_time: float):
        if self.tiempo_advertencia > 0:
            self.tiempo_advertencia -= delta_time
            if self.tiempo_advertencia <= 0:
                self.texto_advertencia = ""

    def actualizar_vida_ui(self, hp_actual: int) -> None:
        self.caja_corazones.clear()

        for n in range(0, hp_actual, 2):
            # Corazón medio para el último punto de vida si hp_actual es impar
            corazon = arcade.gui.UIImage(texture=texturas.UI.CORAZON_MEDIO if n == hp_actual - 1 else texturas.UI.CORAZON_LLENO)
            self.caja_corazones.add(corazon)

    def draw(self):
        # Activar la cámara de la interfaz para dibujar sobre la pantalla, no sobre el mapa
        with self.camara_ui.activate():
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

        self.ui_manager.draw()

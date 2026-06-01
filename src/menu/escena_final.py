import arcade
import arcade.gui as gui
import os


PARRAFOS = [
    "Finalmente Thorne es capaz de vencer a Lucian y con esto acaba así su estadía\nen The Gauntlet.",
    "Es la primera vez que alguien es capaz de encontrar la forma de salir de esta\nprisión de guijarro.",
    "Thorne logra escapar de la prisión que le mantenía encerrado por su gran poder.",
    "Será cosa de tiempo que Cedric sepa de esto y vaya en su búsqueda…",
    "Mientras tanto Thorne solo tiene una posibilidad…",
    "Siempre y cuando no quiera enfrentarse a su hermano, plantarle cara y\nderrocarle.",
    "Si no…",
    "Solo queda huir…",
]


class EscenaFinal(arcade.View):
    def __init__(self):
        super().__init__()

        import os
        os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
        from util import globales
        globales.audio._cargado = False  # Fuerza recargar con la ruta correcta
        globales.audio.reproducir_musica("musica_escena_final", volumen=0.5)

        ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        ruta_fondo = os.path.join(ruta_base, "assets", "images", "fondo_escena_final.png")
        ruta_fuente = os.path.join(ruta_base, "assets", "fonts", "font_escena_final.ttf")

        self.fondo = arcade.load_texture(ruta_fondo)

        try:
            arcade.load_font(ruta_fuente)
            self.nombre_fuente = "EB Garamond"
        except FileNotFoundError:
            self.nombre_fuente = "Arial"

        
        self.indice_actual: int = 0

        # Música
        from util import globales
        globales.audio.reproducir_musica("musica_escena_final", volumen=0.5)

    def on_draw(self):
        self.clear()

        ancho = self.window.width
        alto = self.window.height

        # Fondo
        arcade.draw_texture_rect(self.fondo, arcade.LBWH(0, 0, ancho, alto))

        # Capa semitransparente para que el texto se lea mejor
        arcade.draw_rect_filled(arcade.LBWH(0, 0, ancho, alto), (0, 0, 0, 140))

        # Párrafos visibles hasta el índice actual
        y_inicio = alto * 0.88
        separacion = 75

        for i in range(self.indice_actual + 1):
            y = y_inicio - i * separacion
            arcade.draw_text(
                PARRAFOS[i],
                ancho / 2, y,
                color=(255, 223, 100) if i == self.indice_actual else (200, 200, 200),
                font_size=22,
                font_name=self.nombre_fuente,
                anchor_x="center",
                anchor_y="center",
                multiline=True,
                width=900,
                align="center"
            )

        # Flecha / indicador para continuar
        if self.indice_actual < len(PARRAFOS) - 1:
            arcade.draw_text(
                "▼  Pulsa ENTER para continuar",
                ancho / 2, 25,
                color=(255, 255, 255, 180),
                font_size=16,
                font_name=self.nombre_fuente,
                anchor_x="center",
                anchor_y="center"
            )
        else:
            # Último párrafo: opción de volver al menú
            arcade.draw_text(
                "Pulsa ENTER para volver al menú principal",
                ancho / 2, 60,
                color=(255, 223, 100),
                font_size=16,
                font_name=self.nombre_fuente,
                anchor_x="center",
                anchor_y="center"
            )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            if self.indice_actual < len(PARRAFOS) - 1:
                self.indice_actual += 1
            else:
                from util import globales
                globales.audio.detener_musica()
                from menu.menu_principal import MenuPrincipal
                self.window.show_view(MenuPrincipal())
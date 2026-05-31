
import arcade
import arcade.gui
from util import texturas

class Nivel(arcade.View):
    def __init__(self):
        super().__init__()
        
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        
        self.caja_corazones = arcade.gui.UIBoxLayout(vertical=False, space_between=5)
        
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x='left',
                anchor_y='top',
                align_x=20,
                align_y=-20,
                child=self.caja_corazones
            )
        )
        
    def setup(self):
        # Despues de instanciar al jugador
        # self.jugador = Jugador(...)
        self.actualizar_vida_ui(self.jugador._hp)

    def actualizar_vida_ui(self, hp_actual: int) -> None:
        self.caja_corazones.clear()
        
        for _ in range(hp_actual):
            corazon = arcade.gui.UITextureWidget(
                texture=texturas.UI.CORAZON_LLENO 
            )
            self.caja_corazones.add(corazon)

    def on_draw(self):
        self.clear()
        
        # Código de drawing
        
        self.ui_manager.draw()
# Prueba mapa de ladrillos
import arcade

#import util.io

# Constants
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 500
WINDOW_TITLE = "Ladrillos"

# Constants used to scale our sprites from their original size
TILE_SCALING = 0.5

class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.tile_map = None
        self.scene = None

    def setup(self):

        layer_options = {
            "Platforms": {
                "use_spatial_hash": True
            }
        }

        self.tile_map = arcade.load_tilemap(
            f"assets\maps\\mapa_ladrillos.json",
            scaling=TILE_SCALING,
            layer_options=layer_options,
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE


    def on_draw(self):

        self.clear()

        self.scene.draw()
        


    def on_update(self, delta_time):
        pass




def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
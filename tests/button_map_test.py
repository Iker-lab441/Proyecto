# Pruebas Tile Map
import arcade
import math
import sys
sys.path.append('src')
import util.io
from camara import Camara

#import util.io

# Constants
WINDOW_WIDTH = 810
WINDOW_HEIGHT = 580
WINDOW_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 0.8
PLAYER_JUMP_SPEED = 10

class Jugador(arcade.Sprite):
    _VELOCIDAD: float = 70.0

    def __init__(self, center_x: float, center_y: float):
        super().__init__(":resources:/images/alien/alienBlue_walk1.png", 0.1, center_x, center_y)

    def update(self, delta_time: float):
        super().update(delta_time)

        self.change_x = 0
        if util.io.tecla_mantenida(arcade.key.A) or util.io.tecla_mantenida(arcade.key.LEFT):
            self.change_x -= self._VELOCIDAD * delta_time
        if util.io.tecla_mantenida(arcade.key.D) or util.io.tecla_mantenida(arcade.key.RIGHT):
            self.change_x += self._VELOCIDAD * delta_time

class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.tile_map = None
        self.scene = None
        self.camera = None
        self.gui_camera = None

    def setup(self):

        layer_options = {
            "Platforms": {
                "use_spatial_hash": True
            }
        }

        self.tile_map = arcade.load_tilemap(
            f"assets\maps\\button_map.json",
            scaling=TILE_SCALING,
            layer_options=layer_options,
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.player_sprite = Jugador(10, 18)
        self.scene.add_sprite("Player", self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls=self.scene["Walls"], gravity_constant=GRAVITY
        )

        button_layer = self.tile_map.object_lists["Button"]
        self.button = arcade.SpriteList()

        for button_marker in button_layer:
            coordinates = self.tile_map.get_cartesian(
                button_marker.shape[0], button_marker.shape[1]
            )
            button = arcade.Sprite("assets\images\\BotonRojoPulsado.png",0.5)
            button.center_x = math.floor(
                coordinates[0] * TILE_SCALING * self.tile_map.tile_width
            )
            button.center_y = math.floor(
                (coordinates[1] + 1.8) * (self.tile_map.tile_height * TILE_SCALING)
            )
            self.scene.add_sprite("Button", button)
            self.button.append(button)

        print(self.scene["Button"][0].position)  

        self.camera = Camara()
        self.camera.zoom = 5

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # Calculate the right edge of the map in pixels
        self.end_of_map = (self.tile_map.width * self.tile_map.tile_width)
        self.end_of_map *= self.tile_map.scaling
        print(self.end_of_map)

        self.camera.right_border = self.tile_map.width*18*0.5
        self.camera.top_border = self.tile_map.height*18*0.5

    def on_draw(self):

        self.clear()

        self.camera.use()
        self.button.draw()

        self.scene.draw()
        


    def on_update(self, delta_time):

        util.io.update()

        self.physics_engine.update()

        #self.player_sprite.update(delta_time)

        self.camera.position = self.player_sprite.position

        self.camera.on_update()

    def on_key_press(self, symbol, modifiers):
        util.io.pulsar_tecla(symbol)
        self.player_sprite.update(self.delta_time)
        if self.physics_engine.can_jump(y_distance=10) and (symbol == arcade.key.SPACE):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

    def on_key_release(self, symbol, modifiers):
        util.io.soltar_tecla(symbol)
        self.player_sprite.update(self.delta_time)

    """def on_key_press(self, key, modifiers):

        if key == arcade.key.ESCAPE:
            self.setup()

        if key == arcade.key.SPACE or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0"""


def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
import arcade

import util.io
from util import globales
from menu.menu_principal import MenuPrincipal


class Ventana(arcade.Window):
    def __init__(self) -> None:
        super().__init__()

        self.camara_pos_anterior: arcade.Vec2 = arcade.Vec2(0, 0)
        self.camara_pos: arcade.Vec2 = arcade.Vec2(0, 0)

    def on_update(self, delta_time: float) -> None:
        try:
            self.camara_pos_anterior = self.camara_pos
            self.camara_pos = globales.nivel.camera.bottom_left
        except AttributeError:
            pass

        util.io.mover_raton(util.io.raton_x + self.camara_pos.x - self.camara_pos_anterior.x, util.io.raton_y + self.camara_pos.y - self.camara_pos_anterior.y)
        util.io.update()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        util.io.pulsar_tecla(symbol)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        util.io.soltar_tecla(symbol)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        util.io.pulsar_boton_raton(button)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> None:
        util.io.soltar_boton_raton(button)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        util.io.mover_raton(x + dx + self.camara_pos.x, y + dx + self.camara_pos.y)

def main():
    ventana = Ventana()
    ventana.show_view(MenuPrincipal())
    arcade.run()


if __name__ == "__main__":
    main()

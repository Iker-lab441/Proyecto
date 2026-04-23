import arcade
import util.io
from entidad.jugador import Jugador


class Ventana(arcade.Window):
    def on_update(self, delta_time: float):
        util.io.update()

    def on_draw(self):
        self.clear()

    def on_key_press(self, symbol, modifiers):
        util.io.pulsar_tecla(symbol)

    def on_key_release(self, symbol, modifiers):
        util.io.soltar_tecla(symbol)


def main():
    ventana = Ventana()
    arcade.run()


if __name__ == "__main__":
    main()
import arcade
import util.io


class Ventana(arcade.Window):
    def __init__(self):
        super().__init__()

    def on_update(self, delta_time):
        util.io.update()

    def on_key_press(self, symbol, modifiers):
        util.io.pulsar_tecla(symbol)

    def on_key_release(self, symbol, modifiers):
        util.io.soltar_tecla(symbol)


def main():
    ventana = Ventana()
    arcade.run()


if __name__ == "__main__":
    main()
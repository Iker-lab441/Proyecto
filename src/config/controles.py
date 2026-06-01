import arcade

jugador_izquierda: int = arcade.key.A
jugador_derecha: int = arcade.key.D
jugador_salto: int = arcade.key.SPACE
jugador_abajo: int = arcade.key.S
palanca_interactuar: int = arcade.key.ENTER

boton_disparar: int = arcade.MOUSE_BUTTON_LEFT

menu_debug: int = arcade.key.F1
avanzar_dialogo: int = arcade.key.ENTER
escape: int = arcade.key.ESCAPE

def _cargar_controles() -> None:
    global jugador_izquierda, jugador_derecha, jugador_salto, jugador_abajo, palanca_interactuar
    try:
        with open("controles.txt") as archivo_controles:
            controles = [int(linea) for linea in archivo_controles.readlines()]

            jugador_izquierda = controles[0]
            jugador_derecha = controles[1]
            jugador_salto = controles[2]
            jugador_abajo = controles[3]
            palanca_interactuar = controles[4]
    except FileNotFoundError:
        pass

_cargar_controles()

import arcade 

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
class MiJuego(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sistema de Botón y Puerta")
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        # PRIMERO: Creamos todos los objetos (Sprites)
        self.jugador = arcade.SpriteSolidColor(width=30, height=30, color=arcade.color.BLUE_GRAY)
        self.jugador.center_x = 100
        self.jugador.center_y = 200

        self.boton = arcade.SpriteSolidColor(width=40, height=10, color=arcade.color.RED)
        self.boton.center_x = 300
        self.boton.center_y = 200

        self.puerta = arcade.SpriteSolidColor(width=20, height=80, color=arcade.color.BROWN)
        self.puerta.center_x = 500
        self.puerta.center_y = 200

        self.puerta_abierta = False

        # SEGUNDO: Ahora que ya existen, creamos las listas y el motor
        self.lista_muros = arcade.SpriteList()
        self.lista_muros.append(self.puerta) # Solo la puerta es sólida

        self.physics_engine = arcade.PhysicsEngineSimple(self.jugador, self.lista_muros)

    def on_draw(self):
        self.clear() # Limpia la pantalla
        
        # Dibujamos usando la función global de arcade
        arcade.draw_sprite(self.boton)
        arcade.draw_sprite(self.puerta)
        arcade.draw_sprite(self.jugador)

    def on_update(self, delta_time):
        # 1. Esto hace que el personaje cambie su posición según su velocidad
        # El motor de físicas mueve al jugador y evita que atraviese la lista_muros
            self.physics_engine.update()

        # Lógica de la Puerta (subir)
            if self.puerta_abierta:
                if self.puerta.center_y < 350: 
                    self.puerta.center_y += 1

            if self.puerta_abierta:
    # Si la puerta no ha subido del todo, que siga subiendo
                if self.puerta.center_y < 350: 
                    self.puerta.center_y += 5

        # 2. Esto revisa si pisaste el botón
            if arcade.check_for_collision(self.jugador, self.boton):
                self.puerta_abierta = True
                self.boton.color = arcade.color.GREEN
                self.boton.height = 5
            else:
                self.boton.color = arcade.color.RED
                self.boton.height = 10

        # Evitar que salga por la izquierda o derecha
            if self.jugador.left < 0:
                self.jugador.left = 0
            elif self.jugador.right > SCREEN_WIDTH:
                self.jugador.right = SCREEN_WIDTH

        # Evitar que salga por arriba o abajo
            if self.jugador.bottom < 0:
                self.jugador.bottom = 0
            elif self.jugador.top > SCREEN_HEIGHT:
                self.jugador.top = SCREEN_HEIGHT

    def on_key_press(self, key, modifiers):
        # Movimiento simple para probar
            velocidad = 5
            if key == arcade.key.UP: self.jugador.change_y = velocidad
            elif key == arcade.key.DOWN: self.jugador.change_y = -velocidad
            elif key == arcade.key.LEFT: self.jugador.change_x = -velocidad
            elif key == arcade.key.RIGHT: self.jugador.change_x = velocidad

    def on_key_release(self, key, modifiers):
            if key in [arcade.key.UP, arcade.key.DOWN]: self.jugador.change_y = 0
            if key in [arcade.key.LEFT, arcade.key.RIGHT]: self.jugador.change_x = 0
        
        # Actualizamos la posición del jugador
            self.jugador.update()

if __name__ == "__main__":
    game = MiJuego()
    arcade.run()
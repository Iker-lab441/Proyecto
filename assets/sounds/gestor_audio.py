import arcade

class GestorAudio:
    def __init__(self):
        # 1. Definimos las rutas
        self.ruta_base = "assets/sounds/"
        
        # 2. Diccionario de sonidos
        self.sonidos = {
            "inicio": arcade.load_sound(f"{self.ruta_base}musica_inicio.mp3"),
            "mazmorra": arcade.load_sound(f"{self.ruta_base}ambiente_sotano.mp3"),
            "boton": arcade.load_sound(f"{self.ruta_base}click_boton.wav"),
            "puerta": arcade.load_sound(f"{self.ruta_base}abrir_puerta.wav")
        }
        
        self.reproductor_actual = None

    def reproducir(self, nombre, loop=False, volumen=0.5):
        """Función sencilla para que cualquier compañero la use"""
        if nombre in self.sonidos:
            # Si es música de fondo (loop), guardamos el reproductor para poder pararlo
            if loop:
                self.reproductor_actual = arcade.play_sound(self.sonidos[nombre], volumen, looping=True)
            else:
                arcade.play_sound(self.sonidos[nombre], volumen)

    def detener_musica(self):
        """Para limpiar el sonido antes de cambiar de nivel"""
        if self.reproductor_actual:
            arcade.stop_sound(self.reproductor_actual)
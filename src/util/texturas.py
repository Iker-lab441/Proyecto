import os
import arcade
from pathlib import Path

# Obtenemos la ruta base del proyecto de forma dinámica.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = BASE_DIR / "assets"

def cargar_animacion(ruta, fotogramas) -> list[arcade.Texture]:
    """
    Función de ayuda para acortar código.
    Carga un spritesheet y lo recorta automáticamente en fotogramas de 64x64.
    Devuelve directamente la lista de texturas listas para animar.
    """
    hoja = arcade.load_spritesheet(str(ruta))
    return hoja.get_texture_grid(size=(64, 64), columns=fotogramas, count=fotogramas)


class Jugador:
    # Usamos nuestra nueva pseudo-instrucción 'cargar_animacion'
    # Le pasamos la ruta y la cantidad de fotogramas (basado en el ancho de tus imágenes)
    IDLE = cargar_animacion(ASSETS_DIR / "player" / "thorne_idle_mejorado.png", 6)
    RUN  = cargar_animacion(ASSETS_DIR / "player" / "thorne_andando_mejorado.png", 7)
    JUMP = cargar_animacion(ASSETS_DIR / "player" / "thorne_salto_mejorado.png", 6)
    FALL = cargar_animacion(ASSETS_DIR / "player" / "thorne_aterrizar_mejorado.png", 6)
    
    # Para imágenes simples (1 solo frame), seguimos usando load_texture normal:
    JUMP_LOOP = arcade.load_texture(str(ASSETS_DIR / "player" / "thorne_volar_loop.png"))
    # Añade aquí más animaciones: ATTACK, etc.

class Npcs:
    pass #Eliminar linea de codigo tras implementacion
    #GOBLIN_IDLE = str(ASSETS_DIR / "npcs" / "goblin_idle.png") #No funciona por el momento, hay que hacer el sprite, no descomentar
    # Añade aquí más enemigos: SOMBRAS, LUCIAN (Final Boss), etc.

class UI:
    # Texturas para la interfaz (imágenes simples)
    VIDA_LLENA = arcade.load_texture(str(ASSETS_DIR / "images" / "corazon_lleno.png"))
    VIDA_MEDIO = arcade.load_texture(str(ASSETS_DIR / "images" / "corazon_medio.png"))
    VIDA_VACIA = arcade.load_texture(str(ASSETS_DIR / "images" / "corazon_vacio.png"))

class Mapas:
    pass #Eliminar linea de codigo tras implementacion
    #Todavia no implementado
    #NIVEL_1 = str(ASSETS_DIR / "maps" / "nivel_1.png") # o .tmx si usas Tiled

class Varios:
    pass #Eliminar linea de codigo tras implementacion
    # Objetos, proyectiles, etc. (Todavia sin implementar)
    #ARMADURA_TEMPLARIO = str(ASSETS_DIR / "images" / "armadura.png")

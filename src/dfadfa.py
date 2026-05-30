import numpy as np
from PIL import Image

# Configuración del lienzo técnico (Múltiplos de 64x64)
TILE_SIZE = 64
ROWS, COLS = 3, 4
WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE

# Paleta de colores extraída del sprite del personaje y entorno medieval
VOID = [0, 0, 0, 255]            # #000000 (Vacío absoluto)
SHADOW = [44, 44, 53, 255]       # #2C2C35 (Contornos y juntas oscuras)
BASE_GRAY = [90, 90, 102, 255]   # #5A5A66 (Cuerpo de la piedra)
LIGHT_GRAY = [120, 120, 135, 255]# #787887 (Brillo de bordes)
IRON = [78, 61, 53, 255]         # #4E3D35 (Detalles metálicos / Óxido)
GOLD = [217, 195, 176, 255]     # #D9C3B0 (Brillo de tesoros / Luz)

# Crear el lienzo vacío (Matriz de píxeles RGBA)
pixels = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)

def draw_tile_base(r, c):
    """Genera la textura base de adoquines medievales gastados"""
    y_start, x_start = r * TILE_SIZE, c * TILE_SIZE
    # Rellenar con gris base
    pixels[y_start:y_start+TILE_SIZE, x_start:x_start+TILE_SIZE] = BASE_GRAY
    # Juntas internas de los bloques de piedra
    for i in range(TILE_SIZE):
        pixels[y_start + i, x_start + 31] = SHADOW
        pixels[y_start + 31, x_start + i] = SHADOW
    # Biselado perimetral interno para dar sensación de volumen plano
    pixels[y_start:y_start+2, x_start:x_start+TILE_SIZE] = LIGHT_GRAY
    pixels[y_start:y_start+TILE_SIZE, x_start:x_start+2] = LIGHT_GRAY

# --- FILA 1: SUELOS Y ESTRUCTURAS ---
# Columna 0: Suelo Estándar
draw_tile_base(0, 0)

# Columna 1: Suelo con Grieta Profunda (Muestra el vacío inferior)
draw_tile_base(0, 1)
y, x = 0, TILE_SIZE
for i in range(15, 50):
    offset = int(np.sin(i * 0.5) * 4)
    pixels[y + i, x + 32 + offset : x + 35 + offset] = VOID
    pixels[y + i, x + 31 + offset] = SHADOW

# Columna 2: Rejilla de Ventilación
draw_tile_base(0, 2)
y, x = 0, 2 * TILE_SIZE
pixels[y+16:y+48, x+16:x+48] = SHADOW
for i in range(20, 45, 6):
    pixels[y+16:y+48, x+i : x+i+2] = IRON
    pixels[y+i : y+i+2, x+16:x+48] = IRON

# Columna 3: Pilar Cilíndrico (Visto desde arriba)
draw_tile_base(0, 3)
y, x = 0, 3 * TILE_SIZE
for r_idx in range(24, 0, -1):
    c_color = LIGHT_GRAY if r_idx > 20 else (BASE_GRAY if r_idx > 10 else SHADOW)
    for i in range(TILE_SIZE):
        for j in range(TILE_SIZE):
            if (i-32)**2 + (j-32)**2 < r_idx**2:
                pixels[y+i, x+j] = c_color

# --- FILA 2: ELEMENTOS DE JUEGO (64x64) ---
# Columna 0: Cofre Cerrado
draw_tile_base(1, 0)
y, x = TILE_SIZE, 0
pixels[y+20:y+44, x+14:x+50] = IRON  # Madera base
pixels[y+20:y+44, x+14:x+18] = LIGHT_GRAY # Herraje Izq
pixels[y+20:y+44, x+46:x+50] = LIGHT_GRAY # Herraje Der
pixels[y+28:y+34, x+30:x+34] = GOLD       # Cerradura

# Columna 1: Cofre Abierto (Desplazado con fondo oscuro)
draw_tile_base(1, 1)
y, x = TILE_SIZE, TILE_SIZE
pixels[y+14:y+44, x+14:x+50] = VOID  # Fondo interior expuesto
pixels[y+24:y+40, x+20:x+44] = GOLD  # Oro brillante dentro
pixels[y+6:y+20, x+14:x+50] = IRON   # Tapa volcada hacia arriba

# Columna 2: Trampa de Suelo (Desactivada)
draw_tile_base(1, 2)
y, x = TILE_SIZE, 2 * TILE_SIZE
for i in [20, 32, 44]:
    for j in [20, 32, 44]:
        pixels[y+i:y+i+4, x+j:x+j+4] = VOID

# Columna 3: Trampa de Suelo (Pinchos Activos)
draw_tile_base(1, 3)
y, x = TILE_SIZE, 3 * TILE_SIZE
for i in [20, 32, 44]:
    for j in [20, 32, 44]:
        pixels[y+i:y+i+4, x+j:x+j+4] = VOID
        pixels[y+i+1:y+i+3, x+j+1:x+j+3] = LIGHT_GRAY # Punta metálica

# --- FILA 3: BORDES DE AUTOTILE (Fusión con Vacío) ---
# Columna 0: Borde Norte (El vacío está arriba)
draw_tile_base(2, 0)
y, x = 2 * TILE_SIZE, 0
pixels[y:y+4, x:x+TILE_SIZE] = SHADOW
pixels[y:y+2, x:x+TILE_SIZE] = VOID

# Columna 1: Borde Sur (El vacío está abajo)
draw_tile_base(2, 1)
y, x = 2 * TILE_SIZE, TILE_SIZE
pixels[y+TILE_SIZE-4:y+TILE_SIZE, x:x+TILE_SIZE] = SHADOW
pixels[y+TILE_SIZE-2:y+TILE_SIZE, x:x+TILE_SIZE] = VOID

# Columna 2: Borde Este (El vacío está a la derecha)
draw_tile_base(2, 2)
y, x = 2 * TILE_SIZE, 2 * TILE_SIZE
pixels[y:y+TILE_SIZE, x+TILE_SIZE-4:x+TILE_SIZE] = SHADOW
pixels[y:y+TILE_SIZE, x+TILE_SIZE-2:x+TILE_SIZE] = VOID

# Columna 3: Borde Oeste (El vacío está a la izquierda)
draw_tile_base(2, 3)
y, x = 2 * TILE_SIZE, 3 * TILE_SIZE
pixels[y:y+TILE_SIZE, x:x+4] = SHADOW
pixels[y:y+TILE_SIZE, x:x+2] = VOID

# Guardar la hoja de Tileset optimizada
img = Image.fromarray(pixels, 'RGBA')
img.save("tileset_medieval_64x64.png")
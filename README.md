# The Gaunlet

Videojuego de plataformas y puzles en 2D ambientado en el Abismo, una mazmorra subterránea viva que se alimenta de quienes mueren en ella. Encarna a Thorne, hermano del rey, encarcelado por poseer magia prohibida, y demuestra que eres el verdadero heredero legítimo superando las pruebas del Abismo y venciendo a su guardián final: Lucian.


## Requisitos

- **Python 3.10 o superior** (probado con Python 3.13)
- **Librería Python Arcade**

```bash
pip install arcade
```




## Instalación y ejecución

1. Clona el repositorio o descarga y descomprime el ZIP:

```bash
git clone <url-del-repositorio>
cd Proyecto
```

2. Instala las dependencias:

```bash
pip install arcade
```

3. Ejecuta el juego desde la raíz del proyecto:

```bash
python src/main.py
```

> **Importante:** ejecuta siempre el juego desde la carpeta raíz `Proyecto/`, no desde dentro de `src/`. El juego ajusta automáticamente el directorio de trabajo, pero la ruta de arranque debe ser la raíz del repositorio.




## Controles

Acción:                           | Tecla / Botón:
Moverse izquierda                 | `A` 
Moverse derecha                   | `D` 
Bajar                             | `S`
Saltar                            | `Espacio`
Salto de pared                    | `Espacio` (apoyado en pared)
Disparar proyectil                | `Clic izquierdo` (apunta al ratón)
Interactuar (palancas / puertas)  | `Enter`


Los controles pueden reasignarse desde **Opciones → Asignación de teclas** en el menú principal.



## Cómo jugar

- Desde el menú principal elige **Nueva Partida** para comenzar.
- Al inicio habla con **Fenris**, el mago encerrado que te dará tu armadura y los primeros objetos mágicos.
- Explora cada sala del Abismo, activa palancas y botones para abrir puertas y avanzar.
- Recoge la **llave rúnica** cuando la encuentres: la necesitarás para abrir la puerta de salida de ciertos niveles (pulsa `Enter` junto a ella).
- Evita o elimina a los **goblins** que patrullan las plataformas —antiguos prisioneros corrompidos por la magia del Abismo—; el contacto con ellos te quita vida.
- Al final del camino te espera **Lucian**, la mano derecha del rey Cedric. Esquiva sus embestidas y ráfagas de proyectiles mientras le disparas para derrotarle y escapar del Abismo.
- Tienes **3 corazones** de vida. Si los pierdes todos, el juego termina.




## Estructura del repositorio

```
Proyecto/
├── src/                        # Código fuente
│   ├── main.py                 # Punto de entrada
│   ├── config/                 # Configuración de controles
│   ├── entidad/                # Personajes (jugador, enemigos, proyectiles)
│   ├── menu/                   # Vistas de menús
│   ├── tile/                   # Objetos del mundo (puertas, palancas, botones)
│   └── util/                   # Utilidades (cámara, audio, carga de niveles)
├── assets/
│   ├── images/                 # Sprites, tilesets y fondos
│   ├── maps/                   # Mapas en formato JSON (Tiled)
│   ├── sounds/                 # Música y efectos de sonido
│   └── fonts/                  # Fuentes tipográficas
├── docs/
│   ├── gdd.md                  # Documento de Diseño del Juego
│   └── memoria.md              # Memoria del proyecto
└── README.md                   # Este archivo (instrucciones)
```




## Solución de problemas frecuentes

**El juego no arranca y muestra un error de ruta:**  
Asegúrate de ejecutar `python src/main.py` desde la carpeta raíz `Proyecto/`, no desde dentro de `src/`.

**No se escucha música:**  
Comprueba que la carpeta `assets/sounds/` está presente y contiene los archivos `.mp3` y `.wav`. En Linux, puede ser necesario instalar dependencias de audio de Arcade (`pip install arcade[audio]` o `pip install pyglet`).

**Módulo `arcade` no encontrado:**  
Ejecuta `pip install arcade` o `pip3 install arcade` dependiendo de tu configuración de Python.

**Problema con la codificación de caracteres (Windows):**  
Si ves errores de encoding al cargar los mapas JSON, asegúrate de que la terminal usa UTF-8 o ejecuta el juego desde un entorno virtual.




## Créditos

Desarrollado por el equipo para la asignatura *Tecnología de Videojuegos* — Departamento de Automática, Universidad de Alcalá.

Miembro:        | Rol:
Iker            | Jefe de equipo y programador
Carlos          | Diseñador de niveles principal y programador
Mario           | Diseñador de sonido, botones y programador
Izan            | Diseño de personajes, arte y programador
Kevin           | Historia, diseño narrativo y programador

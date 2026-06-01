# The Gauntlet

Videojuego de plataformas y puzles en 2D ambientado en el Abismo, una mazmorra subterránea viva que se alimenta de quienes mueren en ella. Encarna a Thorne, hermano del rey, encarcelado por poseer magia prohibida, y demuestra que eres el verdadero heredero legítimo superando las pruebas del Abismo y venciendo a su guardián final: Lucian.


## Requisitos

- **Python 3.10 o superior** (probado con Python 3.13) (si la versión es demasiado alta, pymunk, y por lo tanto arcade, fallan al instalarse)
- **Librería Python Arcade**

```bash
pip install arcade
```
o desde requirements.txt
```bash
pip install -r requirements.txt
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
o desde requirements.txt
```bash
pip install -r requirements.txt
```

3. Ejecuta el juego desde la raíz del proyecto:

```bash
python src/main.py
```

> **Importante:** ejecuta siempre el juego desde la carpeta raíz `Proyecto/`, no desde dentro de `src/`




## Controles

Acciones:
- Moverse izquierda: `A` 
- Moverse derecha: `D` 
- Bajar: `S`
- Saltar: `Espacio`
- Salto de pared: `Espacio` (apoyado en pared)
- Disparar proyectil: `Clic izquierdo` (apunta al ratón) (solo funciona en los niveles donde hay enemigos)
- Interactuar (palancas / puertas): `Enter`
- Escape: salir al menú principal


Los controles pueden reasignarse desde **Opciones → Asignación de teclas** en el menú principal.



## Cómo jugar

- Desde el menú principal elige **Nueva Partida** para comenzar.
- Al inicio habla con **Fenris**, el mago encerrado que te introducirá a la mazmorra.
- Explora cada sala del Abismo, activa palancas y botones para abrir puertas y avanzar.
- Recoge la **llave rúnica** cuando la encuentres: la necesitarás para abrir la puerta de salida de los niveles.
- Evita o elimina a los **goblins** que patrullan las plataformas —antiguos prisioneros corrompidos por la magia del Abismo—; el contacto con ellos te quita vida.
- Al final del camino te espera **Lucian**, la mano derecha del rey Cedric. Esquiva sus embestidas y ráfagas de proyectiles mientras le disparas para derrotarle y escapar del Abismo.
- Tienes **3 corazones** de vida. Si los pierdes todos, mueres.




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

Miembros:
- Iker: jefe de equipo y programación
- Carlos: diseñador de niveles principal y programación
- Mario: diseñador de sonido, botones y programación
- Izan: diseño de personajes, arte y programación
- Kevin: historia, diseño narrativo y programación
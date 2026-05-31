# Memoria del proyecto - The Gauntlet

**Asignatura:** Tecnología de Videojuegos
**Departamento:** Automática — Universidad de Alcalá
**Curso:** 2025–2026



## 1. Contexto

Este proyecto se ha desarrollado en el marco de la asignatura transversal *Tecnología de Videojuegos* del Departamento de Automática de la Universidad de Alcalá. El objetivo era diseñar e implementar un videojuego funcional en equipo, aplicando los conceptos de programación orientada a objetos, gestión de eventos, diseño de niveles y control de versiones vistos durante el curso.

El juego resultante, **The Gauntlet**, es un plataformas de acción y puzles en el que el jugador encarna a Thorne, hermano del rey Cedric de Oldegard, encarcelado en el Abismo (una prisión subterránea viva) por poseer magia prohibida. A lo largo del juego debe superar las pruebas del Abismo, derrotar a Lucian (guardián final y mano derecha del rey) y demostrar ser el heredero legítimo.


## 2. Equipo y Roles

Miembro:        | Rol:
- Iker            | Jefe de equipo y programador
- Carlos          | Diseñador de niveles principal y programador
- Mario           | Diseñador de sonido, botones y programador
- Izan            | Diseño de personajes, arte y programador
- Kevin           | Historia, diseño narrativo y programador

La coordinación del grupo se llevó a cabo a través de reuniones periódicas, conversaciones grupales y a través del sistema de issues de GitHub, donde se registraron tareas, bugs, y propuestas de mejora.



## 3. Organización del equipo

En general, todos los miembros del equipo han participado en tareas de programación a lo largo del proyecto, sin una división rígida por áreas. Aun así, cada miembro ha tenido un foco de trabajo más destacado:

- Izan ha sido el principal responsable del arte: creación de sprites, animaciones y assets visuales 2D, además de contribuir a la programación general.
- Mario ha realizado el desarrollo de los menús (menú principal, opciones, asignación de teclas) y el sistema de audio, además de implementar mecanicas de programación como botones o palancas.
- Carlos e Iker han destacado en la creación y diseño de los distintos niveles y mapas, junto con la implementación de las mecánicas de interacción asociadas (puertas, llaves, eventos).
- Kevin ha contribuido a la narrativa, el diseño del juego y la programación de mecánicas generales.



## 4. Grado de Cumplimiento del GDD

### Implementado completamente
- Movimiento del jugador: andar, saltar, salto de pared (wall-jump).
- Sistema de disparo dirigido al cursor del ratón.
- Sistema de vida con 3 corazones y lógica de daño.
- Palancas con dos estados y sistema de callbacks para disparar eventos.
- Botones de colores (amarillo, azul, rojo, verde) con activación por contacto.
- Tres tipos de puertas: estándar, giratoria (gris) e invisible (negra).
- Llave recogible y puerta de salida condicionada a poseerla.
- Goblin perseguidor con IA de patrulla, aggro y persecución.
- Goblin disparador (variante del perseguidor).
- Jefe final (Lucian) con máquina de estados: Idle, Embestida y Disparo.
- Menú principal con música de fondo, botones y tipografía personalizada.
- Menú de ayuda / opciones.
- Menú de asignación de teclas configurable.
- Sistema de audio con música por nivel y efectos de sonido.
- Múltiples niveles: laberinto, parkour, nivel final, sala del jefe.
- Cámara que sigue al jugador.



### No implementado
- Tienda de objetos.
- Modo con/sin checkpoints seleccionable desde el menú.
- Sistema de puntuación o ranking.
- Pantalla de créditos funcional.




## 5. Aspectos Técnicos Destacables

### Arquitectura del código
El proyecto sigue una estructura modular dividida en paquetes:
- `src/entidad/`: clases de todos los personajes (Jugador, Mob, Lucian, Goblins, Proyectil).
- `src/tile/`: objetos del mundo (Puerta, Palanca, Botón, ObjetoEvento).
- `src/menu/`: vistas del menú principal, ayuda, asignación de teclas y debug.
- `src/util/`: utilidades transversales (gestor de audio, cámara, io de entrada, cargador de niveles, texturas, globales).
- `src/config/`: configuración de controles reasignables.


### Máquinas de estados para enemigos y jefe final
El comportamiento de los enemigos se implementó mediante máquinas de estados. Los mobs básicos (goblins) gestionan sus estados (patrulla, idle, aggro, persecución) a través de condiciones encadenadas que controlan la lógica de movimiento en cada frame.
Para el jefe final, Lucian, se optó por una arquitectura más avanzada: cada estado es una clase polimórfica independiente que hereda de la clase abstracta LucianState e implementa su propio método update. Esto permite añadir nuevos patrones de ataque sin modificar la clase principal, simplemente creando una nueva clase de estado y añadiéndola a la secuencia.


### Sistema de eventos (palancas y botones)
Las palancas y botones utilizan listas de *callbacks* (`Callable[[], None]`) para desacoplar el objeto interactuable de los efectos que produce. Esto permite que una sola palanca controle múltiples puertas o efectos de forma flexible.


### Carga de mapas Tiled y clase Nivel
Uno de los mayores retos técnicos del proyecto fue la creación de la clase `Nivel`, que interpreta automáticamente la información del Tilemap trabajando directamente con el diccionario del archivo `.json` sin depender de la capa de abstracción de Arcade. Esto permitió instanciar los sprites según las capas nombradas (`Muros`, `Jugador`, `Goblin`, `Lucian`, `Emisor`, `Receptor`, `Llave`, `Salida`, etc.) y conectar automáticamente los pares emisor/receptor para los mecanismos de activación, pero requirió un análisis profundo de la estructura interna del formato JSON de Tiled.


### Aleatoriedad del laberinto y el minijuego
La generación del laberinto con caminos aleatorios y el movimiento dinámico de la llave en el minijuego supusieron un desafío adicional, ya que era necesario garantizar que el nivel fuera siempre resoluble independientemente de la aleatoriedad introducida.


### Módulo de texturas (`texturas.py`)
Para evitar la carga repetida de sprites y la dependencia constante de la sintaxis interna de Arcade, se desarrolló un módulo centralizado de texturas (`texturas.py`) que precarga todos los assets agrupados en clases (por ejemplo, `texturas.Jugador.IDLE`, `texturas.Npcs.GOBLIN_RUN`, etc.). De esta forma, cualquier parte del código puede acceder a una textura simplemente por su nombre identificativo, sin necesidad de repetir rutas ni llamadas al sistema de carga de Arcade.


### Compatibilidad de rutas
Todas las rutas de assets utilizan `pathlib.Path` con `/` como separador (compatible con Windows, Linux y macOS) y el directorio de trabajo se establece al directorio del archivo principal al arrancar.



## 6. Conclusiones

El equipo ha logrado desarrollar un videojuego de plataformas y puzles completamente jugable, con una arquitectura de código limpia y extensible. Las mecánicas centrales —movimiento, combate, interacción con el entorno y jefe final— funcionan correctamente en Ubuntu (plataforma de evaluación).

El desarrollo en equipo a través de GitHub Issues y commits regulares ha permitido una trazabilidad clara del trabajo individual y colectivo.

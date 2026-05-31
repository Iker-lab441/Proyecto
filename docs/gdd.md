# Documento de Diseño del Juego (GDD)

**Título:** The Gauntlet  
**Género:** Plataformas / Puzle de acción  
**Plataforma:** PC (Windows / Linux / macOS)  
**Motor:** Python + Arcade  
**Estética:** Pixel Art, estilo mazmorra medieval 


## 1. Visión general

The Gauntlet es un videojuego de plataformas y puzles en 2D en el que el jugador encarna a Thorne, hermano menor del rey, encarcelado en una mazmorra subterránea llamada el Abismo tras ser descubierto como portador de magia prohibida. Para escapar debe superar una serie de habitaciones con puzles de lógica rúnica, obstáculos, enemigos y mecanismos de activación. Al superar cada sala, estará más cerca de demostrar su valía, ya que si logra salir, demostrará ser el verdadero heredero legítimo del reino de Oldegard.



## 2. Historia y contexto

Durante la ceremonia de coronación de su hermano Cedric, Thorne es descubierto como portador de una variante de magia prohibida. Cedric, temeroso de un posible golpe de estado, ordena su ejecución secreta. Sin embargo, el consejero real (sin estar totalmente de acuerdo con la sentencia) decide enterrarlo vivo en el Abismo, una prisión subterránea diseñada para anular poderes mágicos.

En secreto, el consejero ha dispuesto pruebas dentro del Abismo para comprobar si Thorne es suficientemente poderoso como para suceder y derrocar a su hermano.

Thorne despierta en el nivel más profundo sin recuerdos claros de cómo descendió, pero con una marca brillante en el brazo. La mazmorra no es solo piedra y rejas: es un ecosistema vivo que se alimenta de la energía de quienes mueren dentro. Fue construida por sus propios antepasados, y sus desafíos son, en realidad, pruebas de linaje. A medida que supera puzles de lógica rúnica y combates contra sombras de antiguos prisioneros, descubre esta verdad.

Al final del camino, Lucian (la mano derecha de Cedric) aguarda como último obstáculo. Derrotarle significa salir del Abismo y demostrar que Thorne es el heredero legítimo.



## 3. Personajes

### 3.1 Thorne (Protagonista)
- Hermano menor del rey Cedric, encarcelado por poseer magia prohibida.
- Al inicio del juego recibe de Fenris una armadura de templario y objetos mágicos.
- **Vida:** 3 puntos de vida (representados con corazones en pantalla).
- **Habilidades:** correr, saltar, salto de pared (wall-jump), disparar proyectiles mágicos con el ratón.
- **Objeto especial:** puede recoger llaves rúnicas para abrir determinadas puertas de salida.

### 3.2 Cedric (Antagonista principal)
- Rey de Oldegard y hermano mayor de Thorne.
- No aparece directamente en el juego, pero es el responsable del encarcelamiento de Thorne.
- Su sombra narrativa se hace presente a través de los diálogos de los NPCs y los mensajes del Abismo.  


### 3.3 Fenris (Mago aliado)

- Mago encerrado en el Abismo por contradecir al reino en múltiples ocasiones.
- Primer NPC que encuentra Thorne. Le proporciona la armadura de templario y objetos mágicos de utilidad.
- Fuente de información sobre la historia del Abismo y el linaje de Thorne.

### 3.4 Goblins (Enemigos)

- Antiguos criminales encerrados en el Abismo que, tras años expuestos a la energía mágica del lugar, han sido corrompidos y se han vuelto seres irracionales que atacan a todo el que se acerque.
- Existen dos variantes implementadas:

**Goblin Perseguidor:**
- Patrulla plataformas de forma aleatoria.
- Al detectar a Thorne en su rango de visión lo persigue activamente.
- Al perderlo de vista vuelve a merodear.
- Quita 1 punto de vida al contacto.

**Goblin Disparador:**
- Variante que también patrulla y tiene sistema de aggro.
- Posee lógica de disparo a distancia.


### 3.5 Lucian (Jefe Final / Antagonista 2)
- Mano derecha de Cedric y guardián final del Abismo.
- Su objetivo es asegurarse de que Thorne no salga jamás de la mazmorra.
- Boss con 30 puntos de vida.
- Alterna entre cuatro patrones de ataque en secuencia predefinida:
  - **Idle:** pausa de 2 segundos entre ataques para dar respiro al jugador.
  - **Embestida:** aparece en uno de varios puntos del mapa y carga en línea recta. Se vuelve intangible durante la preparación.
  - **Disparo:** aparece en posiciones aleatorias y lanza ráfagas de tres proyectiles dirigidos a Thorne con velocidad creciente conforme avanza el combate.
  - **Caida:** aparece en posiciones aleatorias y lanza ráfagas de tres proyectiles dirigidos a Thorne con velocidad creciente conforme avanza el combate.




##  4. Mecánicas de Juego

#### 4.1 Movimiento del Jugador

Acciones:
- Moverse izquierda: `A` 
- Moverse derecha: `D` 
- Bajar: `S`
- Saltar: `Espacio`
- Salto de pared: `Espacio` (apoyado en pared)
- Disparar proyectil: `Clic izquierdo` (apunta al ratón)
- Interactuar (palancas / puertas): `Enter`


### 4.2 Sistema de Vida
- El jugador comienza con 3 vidas (corazones).
- Los enemigos y proyectiles reducen la vida en 1 por impacto.
- Al llegar a 0 el personaje muere.


### 4.3 Palancas
- Objetos interactuables con `Enter`.
- Tienen dos estados: activado / desactivado.
- Al cambiar de estado ejecutan una lista de callbacks (abrir/cerrar puertas, mover plataformas, etc.).


### 4.4 Botones
- Similares a las palancas.
- Se activan al mantenerse sobre ellos o pulsarlos; disparan eventos asociados.


### 4.5 Puertas
Existen tres tipos de puertas:
- **Puerta estándar** (madera): abre/cierra visualmente, bloquea el paso cuando está cerrada.
- **Puerta gris:** gira sobre su eje al abrirse (usa ángulo de rotación).
- **Puerta negra:** desaparece completamente al abrirse (se desplaza fuera de pantalla).


### 4.6 Llave y Puerta de Salida
- Algunos niveles contienen una llave recogible.
- La puerta de salida solo puede abrirse con `Enter` si el jugador lleva la llave.


### 4.7 Proyectiles
- El jugador puede disparar en la dirección del cursor.
- Lucian y otros enemigos también lanzan proyectiles que dañan al jugador.


### 4.8 Salto de Pared (Wall-Jump)
- El jugador puede realizar hasta 1 salto de pared por muro antes de necesitar tocar el suelo.
- Permite escalar paredes verticales alternando lados.




## 5. Niveles y escenas

Mapas:
- `laberinto.json`: primera gran prueba del Abismo: un laberinto de pasillos con caminos ramificados y goblins patrullando
- `minijuego.json`: sala de mecanismos rúnicos: puzles con botones de colores que deben activarse en el orden correcto
- `bloques.json`: zona de plataformas flotantes con bloques de dos colores que reaccionan a los mecanismos
- `parkour.json`: sección de agilidad: saltos encadenados y wall-jumps sobre abismos
- `nivel_final.json`: antesala del guardián: nivel de alta dificultad con goblins y puzles combinados
- `jefe_final.json`: sala de Lucian: combate final contra la mano derecha de Cedric |


La secuencia narrativa es: despertar en el Abismo / encuentro con Fenris → laberinto → puzles de mecanismos → zona de plataformas → parkour → nivel final → combate contra Lucian → salida del Abismo.




## 6. Interfaz de Usuario

### 6.1 Menú Principal
Pantalla con fondo ilustrado y los siguientes botones:
- Nueva Partida
- Continuar
- Opciones
- Créditos
- Salir

Música de fondo en bucle. Fuente tipográfica: *Deutsch Gothic*.

### 6.2 HUD (In-Game)
- Corazones en pantalla que representan los puntos de vida del jugador (lleno / medio / vacío).

### 6.3 Menú de Ayuda (Opciones)
- Accesible desde el menú principal.
- Muestra controles y ajustes básicos.

### 6.4 Menú de Asignación de Teclas
- Permite al jugador reasignar las teclas de control.
- La tecla `Escape` cancela la asignación en curso.

### 6.5 Menú de Debug (`F1`)
- Acceso rápido a distintos niveles de prueba (solo durante desarrollo).




## 7. Arte y Estética

- **Estilo visual:** Pixel art, resolución 1280×720.
- **Paleta:** tonos oscuros de mazmorra (ladrillos, muros con musgo, cadenas, ventanas).
- **Tilesets disponibles:** ladrillo limpio, ladrillo musgoso, ladrillo roto, muros con ventana, muros oxidados, plataformas, rampas.
- **Personajes:** sprites animados con estados Idle / Run / Jump / Fall.
- **Fuente:** Deutsch Gothic (menús).




## 8. Audio

Archivos:
- `musica_menu_principal.mp3`: música del menú principal
- `musica_tutorial.mp3`: música del nivel tutorial
- `musica_nivel_2.mp3`: música nivel 2
- `Musica_rapida_nivel.mp3`: música de niveles de acción
- `musica_final_boss.mp3`: música del jefe final
- `ambiente_nivel_1.mp3`: ambiente del primer nivel
- `salto_protagonista.mp3`: efecto de sonido del salto
- `palanca.wav`: efecto al activar palanca
- `puerta_simple.mp3`: efecto al abrir puerta
- `puerta_grande.mp3`: efecto al abrir puerta grande
- `goblin.mp3`: sonido del goblin
- `grito_goblin.mp3`: grito del goblin al morir
- `boton.mp3`: efecto al pulsar botón



## 9. Tecnología

- **Lenguaje:** Python 3.13
- **Librería principal:** Python Arcade
- **Mapas:** Tiled (formato JSON / TMJ)
- **Gestión de rutas:** `pathlib.Path` y `os.path` para compatibilidad multiplataforma
- **Control de versiones:** Git / GitHub (rama `main`)




## 10. Equipo

Miembros:
- Iker: jefe de equipo y programador
- Carlos: diseñador de niveles principal y programador
- Mario: diseñador de sonido, botones y programador
- Izan: diseño de personajes, arte y programador
- Kevin: historia, diseño narrativo y programador
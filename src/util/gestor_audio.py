import arcade
from pathlib import Path


_RUTA_BASE = Path("assets") / "sounds"


class GestorAudio:
    def __init__(self):
        self.sonidos: dict[str, arcade.Sound] = {}
        self._reproductor_musica = None
        self._cargado: bool = False

    def _cargar(self) -> None:
        """Carga diferida: se llama la primera vez que se usa el gestor,
        cuando Arcade ya tiene su ventana inicializada y no falla con el audio."""
        if self._cargado:
            return
        self._cargado = True

        archivos = {
            # Música de fondo
            "musica_menu":     _RUTA_BASE / "musica_menu_principal.mp3",
            "musica_tutorial": _RUTA_BASE / "musica_nivel_tutorial.mp3",
            "musica_nivel_1":  _RUTA_BASE / "ambiente_nivel_1.mp3",
            "musica_nivel_2":  _RUTA_BASE / "musica_nivel_2.mp3",
            "musica_rapida":   _RUTA_BASE / "Musica_rapida_nivel.mp3",
            "musica_boss":     _RUTA_BASE / "musica_final_boss.mp3",
            # Efectos de sonido
            "salto":           _RUTA_BASE / "salto_protagonista.mp3",
            "palanca":         _RUTA_BASE / "palanca.wav",
            "boton":           _RUTA_BASE / "boton.mp3",
            "puerta":          _RUTA_BASE / "puerta_simple.mp3",
            "puerta_grande":   _RUTA_BASE / "puerta_grande.mp3",
            "goblin":          _RUTA_BASE / "goblin.mp3",
            "grito_goblin":    _RUTA_BASE / "grito_goblin.mp3",
            "daño_protagonista":  _RUTA_BASE / "daño_protagonista.mp3",
            "muerte_protagonista":_RUTA_BASE / "muerte_protagonista.mp3",  
            "daño_lucian":        _RUTA_BASE / "daño_lucian.mp3",          
            "muerte_lucian":      _RUTA_BASE / "muerte_lucian.mp3",       
            "ataque_lucian":      _RUTA_BASE / "ataque_lucian.mp3",        
            "disparo_lucian":     _RUTA_BASE / "disparo.mp3",
            "musica_escena_final":  _RUTA_BASE / "musica_escena_final.mp3",
        }

        for nombre, ruta in archivos.items():
            try:
                self.sonidos[nombre] = arcade.load_sound(ruta)
            except Exception as e:
                print(f"[GestorAudio] No se pudo cargar '{nombre}' ({ruta}): {e}")


    def reproducir(self, nombre: str, volumen: float = 0.5) -> None:
        """Reproduce un efecto de sonido puntual (sin bucle)."""
        self._cargar()
        sonido = self.sonidos.get(nombre)
        if sonido:
            arcade.play_sound(sonido, volumen)

    def reproducir_musica(self, nombre: str, volumen: float = 0.4) -> None:
        """Para la música actual y arranca la nueva en bucle."""
        self._cargar()
        self.detener_musica()
        sonido = self.sonidos.get(nombre)
        if sonido:
            self._reproductor_musica = arcade.play_sound(sonido, volumen, loop=True)

    def detener_musica(self) -> None:
        """Para la música de fondo."""
        if self._reproductor_musica:
            try:
                arcade.stop_sound(self._reproductor_musica)
            except Exception:
                pass
            self._reproductor_musica = None
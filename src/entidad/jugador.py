import arcade

from entidad.mob import Mob
from entidad.flecha import Flecha
from menu.menu_principal import MenuPrincipal
import util.io
from util import texturas, globales
import config.controles as controles


class Jugador(Mob):
    _VELOCIDAD_SALTO: float = 20.0
    _MAX_SALTO_MURO: int = 1
    _COOLDOWN_PROYECTIL: float = 0.25

    def __init__(self, scale: float, center_x: float, center_y: float) -> None:
        super().__init__(hp=6, velocidad_base=600, frames_por_textura=10, texture=texturas.Jugador.IDLE[0], scale=scale, center_x=center_x, center_y=center_y)

        self._contador_salto_muro: int = 0
        self._ultimo_muro_saltado_x: float = 0

        self._aterrizando: bool = True
        self._cooldown_proyectil: float = 0

        self._cambiar_animacion(texturas.Jugador.JUMP_LOOP)

        self._muerto: bool = False
        self._has_llave: bool = False

    def update(self, delta_time: float) -> None:
        super().update(delta_time)

        self._cooldown_proyectil -= delta_time

        if self._en_suelo:
            # Si está en el suelo, reinicia el salto de pared
            self._contador_salto_muro = 0

        self._andar(delta_time)
        self._saltar(delta_time)
        self._disparar(delta_time)

        if util.io.tecla_justo_soltada(controles.escape):
            globales.nivel.window.show_view(MenuPrincipal())

    def _andar(self, delta_time: float) -> None:
        self.change_x = 0

        if util.io.tecla_mantenida(controles.jugador_izquierda):
            self.change_x -= self._velocidad_base * delta_time

        if util.io.tecla_mantenida(controles.jugador_derecha):
            self.change_x += self._velocidad_base * delta_time

        # Si andar le mete en una pared, se queda quieto
        if self._a_punto_de_chocarse_con_pared():
            self.change_x = 0

    def _saltar(self, delta_time: float) -> None:
        if util.io.tecla_justo_pulsada(controles.jugador_salto):
            if self._en_suelo or (self._en_pared and (self._contador_salto_muro < self._MAX_SALTO_MURO or self._saltando_nuevo_muro(delta_time))):
                self._contador_salto_muro = 0
                self.change_y = self._VELOCIDAD_SALTO
                self._aterrizando = True
                globales.audio.reproducir("salto", volumen=2)
                if not self._en_suelo:
                    if self._saltando_nuevo_muro(delta_time):
                        self._ultimo_muro_saltado_x = self.center_x
                        self._contador_salto_muro = 0
                    self._contador_salto_muro += 1

    def _saltando_nuevo_muro(self, delta_time: float) -> bool:
        return abs(self.center_x - self._ultimo_muro_saltado_x) > self._velocidad_base * delta_time * 2

    def _disparar(self, delta_time: float) -> None:
        # Con las cámaras especiales que tienen algunos niveles, parece que los proyectiles no se disparan al sitio correcto. Por eso se limita en qué niveles se puede disparar
        if globales.nivel.path_mapa.stem != "nivel_final" and globales.nivel.path_mapa.stem != "jefe_final":
            return

        if self._cooldown_proyectil <= 0 and (util.io.boton_raton_mantenido(controles.boton_disparar) or util.io.tecla_mantenida(controles.boton_disparar)):
            self._cooldown_proyectil = self._COOLDOWN_PROYECTIL
            direccion_proyectil = arcade.Vec2(util.io.raton_x - self.center_x, util.io.raton_y - self.center_y).normalize() * self._velocidad_base / 30
            globales.nivel.add_proyectil(Flecha(direccion_proyectil.x, direccion_proyectil.y, self))

    def update_animation(self, delta_time: float) -> None:
        self._avanzar_animacion()

        if self.change_x != 0:
            self.scale_x = abs(self.scale_x) * util.signo(self.change_x)

        if self._en_suelo:
            if self._aterrizando:
                if self.textures is texturas.Jugador.JUMP_LOOP:
                    self._cambiar_animacion(texturas.Jugador.FALL)
                elif self.textures is texturas.Jugador.FALL and self.cur_texture_index // self._frames_por_textura >= len(self.textures):
                    self._aterrizando = False
                    self._cambiar_animacion(texturas.Jugador.IDLE)
            elif self.change_x == 0:
                self._cambiar_animacion(texturas.Jugador.IDLE)
            else:
                self._cambiar_animacion(texturas.Jugador.RUN)
        elif self.change_y > 0:
            self._cambiar_animacion(texturas.Jugador.JUMP)
        else:
            self._cambiar_animacion(texturas.Jugador.JUMP_LOOP)

        self._mostrar_animacion()

    def kill(self) -> None:
        from util.nivel import Nivel
        globales.nivel.window.show_view(Nivel(globales.nivel.tilemap.path))

    def dañar(self, daño: int = 1) -> None:
        super().dañar(daño)
        globales.nivel.interfaz.actualizar_vida_ui(self._hp)
    @property
    def esta_muerto(self) -> bool:
        return self._muerto

    @property
    def en_suelo(self) -> bool:
        return self._en_suelo

    @property
    def has_llave(self) -> bool:
        return self._has_llave

    @has_llave.setter
    def has_llave(self, valor: bool) -> None:
        self._has_llave = valor
        globales.nivel.interfaz.mostrar_advertencia("Llave obtenida")

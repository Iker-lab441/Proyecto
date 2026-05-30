import arcade

from entidad.mob import Mob
import util.io
import util.texturas as texturas
import config.controles as controles


class Jugador(Mob):
    _VELOCIDAD_SALTO: float = 20.0
    _MAX_SALTO_MURO: int = 1
    _FRAMES_PER_ANIM: int = 10

    def __init__(self, scale: float, center_x: float, center_y: float) -> None:
        super().__init__(hp=3, velocidad_base=600, texture=texturas.Jugador.IDLE[0], scale=scale, center_x=center_x, center_y=center_y)

        self._contador_salto_muro: int = 0
        self._ultimo_muro_saltado_x: float = 0

        self._aterrizando: bool = True

        self._cambiar_anim(texturas.Jugador.JUMP_LOOP)

    def update(self, delta_time: float) -> None:
        super().update(delta_time)

        if self._en_suelo:
            # Si está en el suelo, reinicia el salto de pared
            self._contador_salto_muro = 0

        self._andar(delta_time)
        self._saltar(delta_time)

    def _andar(self, delta_time: float) -> None:
        self.change_x = 0

        if util.io.tecla_mantenida(controles.jugador_izquierda):
            self.change_x -= self._velocidad_base * delta_time

        if util.io.tecla_mantenida(controles.jugador_derecha):
            self.change_x += self._velocidad_base * delta_time

        # Si andar le mete en una pared, se queda quieto
        if self.a_punto_de_chocarse_con_pared():
            self.change_x = 0

    def _saltar(self, delta_time: float) -> None:
        if util.io.tecla_justo_pulsada(controles.jugador_salto):
            if self._en_suelo or (self._en_pared and (self._contador_salto_muro < self._MAX_SALTO_MURO or self._saltando_nuevo_muro(delta_time))):
                self._contador_salto_muro = 0
                self.change_y = self._VELOCIDAD_SALTO
                self._aterrizando = True
                if not self._en_suelo:
                    if self._saltando_nuevo_muro(delta_time):
                        self._ultimo_muro_saltado_x = self.center_x
                        self._contador_salto_muro = 0
                    self._contador_salto_muro += 1

    def _saltando_nuevo_muro(self, delta_time: float) -> bool:
        return abs(self.center_x - self._ultimo_muro_saltado_x) > self._velocidad_base * delta_time * 2

    def update_animation(self, delta_time: float) -> None:
        self.cur_texture_index += 1

        if self.change_x != 0:
            self.scale_x = abs(self.scale_x) * util.signo(self.change_x)

        if self._en_suelo:
            if self._aterrizando:
                if self.textures is texturas.Jugador.JUMP_LOOP:
                    self._cambiar_anim(texturas.Jugador.FALL)
                elif self.textures is texturas.Jugador.FALL and self.cur_texture_index // self._FRAMES_PER_ANIM >= len(self.textures):
                    self._aterrizando = False
                    self._cambiar_anim(texturas.Jugador.IDLE)
            elif self.change_x == 0:
                self._cambiar_anim(texturas.Jugador.IDLE)
            else:
                self._cambiar_anim(texturas.Jugador.RUN)
        elif self.change_y > 0:
            self._cambiar_anim(texturas.Jugador.JUMP)
        else:
            self._cambiar_anim(texturas.Jugador.JUMP_LOOP)

        self.cur_texture_index %= len(self.textures) * self._FRAMES_PER_ANIM
        self.texture = self.textures[self.cur_texture_index // self._FRAMES_PER_ANIM]

    def _cambiar_anim(self, anim: list[arcade.Texture]) -> None:
        if self.textures is not anim:
            self.cur_texture_index = 0
            self.textures = anim

    def dañar(self) -> None:
        self._hp -= 1
        if self._hp == 0:
            self._muerto = True

    @property
    def esta_muerto(self) -> bool:
        return self._muerto

    @property
    def en_suelo(self) -> bool:
        return self._en_suelo

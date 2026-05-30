import arcade

import util.io
import util.texturas as texturas
import config.controles as controles


class Jugador(arcade.Sprite):
    _VELOCIDAD: float = 600.0
    _VELOCIDAD_SALTO: float = 20.0
    _MAX_SALTO_MURO: int = 1
    _HP: int = 3
    _FRAMES_PER_ANIM: int = 10

    def __init__(self, scale: float, center_x: float, center_y: float, distancia_al_suelo: float, muros: arcade.SpriteList[arcade.Sprite]) -> None:
        super().__init__(texturas.Jugador.IDLE[0], scale, center_x, center_y)

        self._distancia_al_suelo: float = distancia_al_suelo
        self._muros: arcade.SpriteList[arcade.Sprite] = muros
        self._contador_salto_muro: int = 0
        self._ultimo_muro_saltado: float = 0

        self._en_suelo: bool = True
        self._en_muro: bool = False
        self._aterrizando: bool = False
        self._can_jump: bool = False

        self._velocidad = self._VELOCIDAD
        self._hp: int = self._HP
        self._muerto: bool = False

    def update(self, delta_time: float) -> None:
        self._comprobar_salto(delta_time)
        self._velocidad = self._VELOCIDAD if self._en_suelo else self._VELOCIDAD * 0.8

        if self.change_x != 0:
            self.scale_x = util.signo(self.change_x) * abs(self.scale_x)

        self._andar(delta_time)
        self._saltar(delta_time)

    def _comprobar_salto(self, delta_time: float) -> None:
        # Comprueba si está en el suelo
        self.center_y -= self._distancia_al_suelo
        self._en_suelo = bool(self.collides_with_list(self._muros))
        self.center_y += self._distancia_al_suelo

        if self._en_suelo:
            # Si está en el suelo, reinicia el salto de pared
            self._en_muro = False
            self._contador_salto_muro = 0
        else:
            # Si no está en el suelo, comprueba el salto de pared en ambas direcciones
            self.center_x += self._velocidad * delta_time
            self._en_muro = bool(self.collides_with_list(self._muros))
            self.center_x -= self._velocidad * delta_time
            if not self._en_muro:
                self.center_x -= self._velocidad * delta_time
                self._en_muro = bool(self.collides_with_list(self._muros))
                self.center_x += self._velocidad * delta_time

    def _andar(self, delta_time: float) -> None:
        self.change_x = 0

        if util.io.tecla_mantenida(controles.jugador_izquierda):
            self.change_x -= self._velocidad * delta_time

        if util.io.tecla_mantenida(controles.jugador_derecha):
            self.change_x += self._velocidad * delta_time

        # Si andar le mete en una pared, se queda quieto
        change_x = self.change_x
        self.center_x += change_x
        if self.collides_with_list(self._muros):
            self.change_x = 0
        self.center_x -= change_x

    def _saltar(self, delta_time: float) -> None:
        if util.io.tecla_justo_pulsada(controles.jugador_salto):
            if self._can_jump or self._en_muro and (self._contador_salto_muro < self._MAX_SALTO_MURO or self._saltando_nuevo_muro(delta_time)):
                self.change_y = self._VELOCIDAD_SALTO
                self._aterrizando = True
                if self._en_muro:
                    if self._saltando_nuevo_muro(delta_time):
                        self._ultimo_muro_saltado = self.center_x
                        self._contador_salto_muro = 0
                    self._contador_salto_muro += 1

    def _saltando_nuevo_muro(self, delta_time: float) -> bool:
        return abs(self.center_x - self._ultimo_muro_saltado) > self._velocidad * delta_time * 2

    def update_animation(self, delta_time: float) -> None:
        self.cur_texture_index += 1

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
                scale_x_anterior = self.scale_x
                self.scale_x = abs(scale_x_anterior) * util.signo(self.change_x)

                if self.scale_x != scale_x_anterior:
                    self.cur_texture_index = 0

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

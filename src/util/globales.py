import arcade

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entidad.jugador import Jugador
    from util.nivelazo import Nivel

from util.gestor_audio import GestorAudio

nivel: "Nivel"
jugador: "Jugador"
suelos: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
paredes: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()

audio: GestorAudio = GestorAudio()
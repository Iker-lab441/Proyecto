import arcade

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entidad.jugador import Jugador


jugador: "Jugador"
suelos: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
paredes: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
import arcade


class ObjetoEvento(arcade.Sprite):
    def __init__(self, interaccion1: function, interaccion2: function, path_or_texture = None, scale = 1, center_x = 0, center_y = 0, angle = 0, **kwargs):
        super().__init__(path_or_texture, scale, center_x, center_y, angle, **kwargs)
        self._interaccion1: function = interaccion1
        self._interaccion2: function = interaccion2
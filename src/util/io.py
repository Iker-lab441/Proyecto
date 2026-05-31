_teclas: dict[int, bool] = {}
_teclas_justo_pulsadas: dict[int, bool] = {}
_teclas_justo_soltadas: dict[int, bool] = {}

_botones_raton: dict[int, bool] = {}
_botones_raton_justo_pulsados: dict[int, bool] = {}
_botones_raton_justo_soltados: dict[int, bool] = {}

raton_x: float = 0
raton_y: float = 0


def pulsar_tecla(tecla: int) -> None:
    _teclas[tecla] = True
    _teclas_justo_pulsadas[tecla] = True


def soltar_tecla(tecla: int) -> None:
    _teclas[tecla] = False
    _teclas_justo_soltadas[tecla] = True


def pulsar_boton_raton(boton: int) -> None:
    _botones_raton[boton] = True
    _botones_raton_justo_pulsados[boton] = True


def soltar_boton_raton(boton: int) -> None:
    _botones_raton[boton] = False
    _botones_raton_justo_soltados[boton] = True


def mover_raton(x: float, y: float) -> None:
    global raton_x, raton_y

    raton_x = x
    raton_y = y


def update() -> None:
    global _teclas_justo_pulsadas, _teclas_justo_soltadas, _botones_raton_justo_pulsados, _botones_raton_justo_soltados

    _teclas_justo_pulsadas = {}
    _teclas_justo_soltadas = {}

    _botones_raton_justo_pulsados = {}
    _botones_raton_justo_soltados = {}


def tecla_justo_pulsada(tecla: int) -> bool:
    return _teclas_justo_pulsadas.get(tecla, False)


def tecla_justo_soltada(tecla: int) -> bool:
    return _teclas_justo_soltadas.get(tecla, False)


def tecla_mantenida(tecla: int) -> bool:
    return _teclas.get(tecla, False)


def boton_raton_justo_pulsado(boton: int) -> bool:
    return _botones_raton_justo_pulsados.get(boton, False)


def boton_raton_justo_soltado(boton: int) -> bool:
    return _botones_raton_justo_soltados.get(boton, False)


def boton_raton_mantenido(boton: int) -> bool:
    return _botones_raton.get(boton, False)

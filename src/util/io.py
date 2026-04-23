_teclas: dict[int, bool] = {}
_teclas_justo_pulsadas: dict[int, bool] = {}
_teclas_justo_soltadas: dict[int, bool] = {}


def pulsar_tecla(tecla: int) -> None:
    _teclas[tecla] = True
    _teclas_justo_pulsadas[tecla] = True


def soltar_tecla(tecla: int) -> None:
    _teclas[tecla] = False
    _teclas_justo_soltadas[tecla] = True


def update() -> None:
    global _teclas_justo_pulsadas, _teclas_justo_soltadas
    _teclas_justo_pulsadas = {}
    _teclas_justo_soltadas = {}


def tecla_justo_pulsada(tecla: int) -> bool:
    return _teclas_justo_pulsadas.get(tecla, False)


def tecla_justo_soltada(tecla: int) -> bool:
    return _teclas_justo_soltadas.get(tecla, False)


def tecla_mantenida(tecla: int) -> bool:
    return _teclas.get(tecla, False)
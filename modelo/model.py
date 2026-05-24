from abc import ABC, abstractmethod


# ─────────────────────────────────────────
# EXCEPCIONES PERSONALIZADAS
# ─────────────────────────────────────────
class FoodUError(Exception):
    """Excepcion base del sistema FoodU"""
    pass

class ProductoNoEncontradoError(FoodUError):
    def __init__(self, producto_id):
        super().__init__(f"No se encontro un producto con el ID {producto_id}")

class PuntuacionInvalidaError(FoodUError):
    def __init__(self, puntuacion):
        super().__init__(f"La puntuacion {puntuacion} no es valida. Debe estar entre 1 y 5")

class UsuarioDuplicadoError(FoodUError):
    def __init__(self, campo):
        super().__init__(f"Error: ese {campo} ya esta registrado")

class VendedorDuplicadoError(FoodUError):
    def __init__(self, nombre):
        super().__init__(f"Error: el vendedor '{nombre}' ya existe")

class PedidoVacioError(FoodUError):
    def __init__(self):
        super().__init__("El pedido debe tener al menos un producto")
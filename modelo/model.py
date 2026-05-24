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



# ─────────────────────────────────────────
# CLASE ABSTRACTA BASE — ABSTRACCION Y HERENCIA
# ─────────────────────────────────────────
class Persona(ABC):
    """Clase abstracta base para Usuario y Vendedor"""

    def __init__(self, nombre: str, contrasena: str):
        self.__nombre = nombre
        self.__contrasena = contrasena

    @property
    def nombre(self):
        return self.__nombre

    @property
    def contrasena(self):
        return self.__contrasena

    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        if not nuevo_nombre or len(nuevo_nombre) <= 2:
            raise ValueError("El nombre debe tener mas de 2 caracteres")
        self.__nombre = nuevo_nombre

    @contrasena.setter
    def contrasena(self, nueva_contrasena: str):
        if len(nueva_contrasena) < 4:
            raise ValueError("La contrasena debe tener al menos 4 caracteres")
        self.__contrasena = nueva_contrasena

    @abstractmethod
    def __str__(self):
        pass
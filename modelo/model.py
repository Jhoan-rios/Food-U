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


# ─────────────────────────────────────────
# PRODUCTO
# ─────────────────────────────────────────
class Producto:
    def __init__(self, producto_id: int, nombre: str, precio: float, tiempo_preparacion: int, disponible: bool):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        if tiempo_preparacion <= 0:
            raise ValueError("El tiempo de preparacion debe ser mayor a 0")
        self.id: int = producto_id
        self.__nombre: str = nombre
        self.__precio: float = precio
        self.__tiempo_preparacion: int = tiempo_preparacion
        self.disponible: bool = disponible

    @property
    def nombre(self):
        return self.__nombre

    @property
    def precio(self):
        return self.__precio

    @property
    def tiempo_preparacion(self):
        return self.__tiempo_preparacion

    @nombre.setter
    def nombre(self, valor):
        if not valor:
            raise ValueError("El nombre del producto no puede estar vacio")
        self.__nombre = valor

    @precio.setter
    def precio(self, valor):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo")
        self.__precio = valor

    @tiempo_preparacion.setter
    def tiempo_preparacion(self, valor):
        if valor <= 0:
            raise ValueError("El tiempo de preparacion debe ser mayor a 0")
        self.__tiempo_preparacion = valor

    def actualizar_disponibilidad(self, estado: bool):
        self.disponible = estado

    def __str__(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return f"[{self.id}] {self.__nombre} - ${self.__precio} | {self.__tiempo_preparacion} min | {estado}"
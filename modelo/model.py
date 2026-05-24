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



# ─────────────────────────────────────────
# PEDIDO
# ─────────────────────────────────────────
class Pedido:
    ESTADOS_VALIDOS = ["pendiente", "en preparacion", "listo", "entregado", "cancelado"]

    def __init__(self, pedido_id: int, usuario: "Usuario"):
        self.id: int = pedido_id
        self.usuario: Usuario = usuario
        self.productos: list[Producto] = []
        self.__estado: str = "pendiente"
        self.tiempo_estimado: int = 0
        self.total: float = 0.0

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        self.__estado = valor

    def calcular_tiempo(self):
        if not self.productos:
            raise PedidoVacioError()
        mayor = 0
        for p in self.productos:
            if p.tiempo_preparacion > mayor:
                mayor = p.tiempo_preparacion
        self.tiempo_estimado = mayor
        return self.tiempo_estimado

    def calcular_total(self):
        if not self.productos:
            raise PedidoVacioError()
        suma = 0
        for p in self.productos:
            suma = suma + p.precio
        self.total = suma
        return self.total

    def cambiar_estado(self, nuevo_estado: str):
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado '{nuevo_estado}' no valido.")
        self.__estado = nuevo_estado

    def __str__(self):
        texto = f"Pedido #{self.id} | Estado: {self.__estado}\n"
        texto += f"  Usuario: {self.usuario.nombre}\n"
        texto += f"  Productos:\n"
        for p in self.productos:
            texto += f"    - {p.nombre} ${p.precio}\n"
        texto += f"  Tiempo estimado: {self.tiempo_estimado} min\n"
        texto += f"  Total: ${self.total}"
        return texto


# ─────────────────────────────────────────
# USUARIO — hereda de Persona
# ─────────────────────────────────────────
class Usuario(Persona):
    def __init__(self, usuario_id: int, nombre: str, correo: str, tiempo_disponible: int, contrasena: str):
        super().__init__(nombre, contrasena)
        self.id: int = usuario_id
        self.__correo: str = correo
        self.tiempo_disponible: int = tiempo_disponible
        self.historial_pedidos: list[Pedido] = []

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if "@" not in valor:
            raise ValueError("El correo no es valido")
        self.__correo = valor

    def realizar_pedido(self, productos: list):
        if not productos:
            raise PedidoVacioError()
        id_nuevo = len(self.historial_pedidos) + 1
        pedido = Pedido(id_nuevo, self)
        pedido.productos = productos
        pedido.calcular_tiempo()
        pedido.calcular_total()
        self.historial_pedidos.append(pedido)
        return pedido

    def ver_historial(self):
        return self.historial_pedidos

    def calificar_vendedor(self, vendedor: "Vendedor", puntuacion: int):
        if not (1 <= puntuacion <= 5):
            raise PuntuacionInvalidaError(puntuacion)
        if vendedor.calificacion == 0:
            vendedor.calificacion = puntuacion
        else:
            vendedor.calificacion = (vendedor.calificacion + puntuacion) / 2

    def __str__(self):
        return f"Usuario: {self.nombre} | Correo: {self.__correo}"
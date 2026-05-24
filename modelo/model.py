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
    def __init__(self, producto_id: int, nombre: str, precio: float, tiempo_preparacion: int, disponible: bool, imagen: str = ""):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        if tiempo_preparacion <= 0:
            raise ValueError("El tiempo de preparacion debe ser mayor a 0")
        self.id: int = producto_id
        self.__nombre: str = nombre
        self.__precio: float = precio
        self.__tiempo_preparacion: int = tiempo_preparacion
        self.disponible: bool = disponible
        self.imagen: str = imagen

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





# ─────────────────────────────────────────
# VENDEDOR — hereda de Persona
# ─────────────────────────────────────────
class Vendedor(Persona):
    def __init__(self, nombre: str, contrasena: str):
        super().__init__(nombre, contrasena)
        self.productos: list[Producto] = []
        self.pedidos_activos: list = []
        self.calificacion: float = 0.0

    def agregar_producto(self, producto: Producto):
        if not isinstance(producto, Producto):
            raise TypeError("Solo se pueden agregar objetos de tipo Producto")
        self.productos.append(producto)

    def editar_producto(self, producto_id: int, nuevo_nombre: str, nuevo_precio: float,
                        nuevo_tiempo: int, nueva_disponibilidad: bool):
        for p in self.productos:
            if p.id == producto_id:
                p.nombre = nuevo_nombre
                p.precio = nuevo_precio
                p.tiempo_preparacion = nuevo_tiempo
                p.disponible = nueva_disponibilidad
                return
        raise ProductoNoEncontradoError(producto_id)

    def eliminar_producto(self, producto_id: int):
        for p in self.productos:
            if p.id == producto_id:
                self.productos.remove(p)
                return
        raise ProductoNoEncontradoError(producto_id)

    def gestionar_pedidos(self):
        return self.pedidos_activos

    def __str__(self):
        return f"Vendedor: {self.nombre} | Calificacion: {self.calificacion}"




# ─────────────────────────────────────────
# RECOMENDADOR
# ─────────────────────────────────────────
class Recomendador:
    def recomendar(self, usuario: Usuario, todos_productos: list):
        try:
            if len(usuario.historial_pedidos) == 0:
                disponibles = [p for p in todos_productos if p.disponible]
                for i in range(len(disponibles)):
                    for j in range(i + 1, len(disponibles)):
                        if disponibles[i].precio > disponibles[j].precio:
                            disponibles[i], disponibles[j] = disponibles[j], disponibles[i]
                return disponibles[:3]

            conteo = {}
            for pedido in usuario.historial_pedidos:
                for producto in pedido.productos:
                    conteo[producto.id] = conteo.get(producto.id, 0) + 1

            disponibles = [p for p in todos_productos if p.disponible]
            for i in range(len(disponibles)):
                for j in range(i + 1, len(disponibles)):
                    veces_i = conteo.get(disponibles[i].id, 0)
                    veces_j = conteo.get(disponibles[j].id, 0)
                    if veces_i < veces_j:
                        disponibles[i], disponibles[j] = disponibles[j], disponibles[i]
            return disponibles[:3]

        except Exception as e:
            print(f"Error al generar recomendaciones: {e}")
            return []


# ─────────────────────────────────────────
# SISTEMA FOODU
# ─────────────────────────────────────────
class SistemaFoodU:
    def __init__(self):
        self.usuarios: list = []
        self.vendedores: list = []
        self.pedidos: list = []
        self.recomendador = Recomendador()

    def registrar_usuario(self, usuario: Usuario):
        try:
            for u in self.usuarios:
                if u.nombre == usuario.nombre:
                    raise UsuarioDuplicadoError("nombre de usuario")
                if u.correo == usuario.correo:
                    raise UsuarioDuplicadoError("correo")
            self.usuarios.append(usuario)
            return "Usuario registrado correctamente"
        except UsuarioDuplicadoError as e:
            return str(e)

    def registrar_vendedor(self, vendedor: Vendedor):
        try:
            for v in self.vendedores:
                if v.nombre == vendedor.nombre:
                    raise VendedorDuplicadoError(vendedor.nombre)
            self.vendedores.append(vendedor)
            return "Vendedor registrado correctamente"
        except VendedorDuplicadoError as e:
            return str(e)

    def crear_pedido(self, usuario: Usuario, productos: list):
        if not productos:
            raise PedidoVacioError()
        pedido = usuario.realizar_pedido(productos)
        self.pedidos.append(pedido)
        for vendedor in self.vendedores:
            for p in productos:
                if p in vendedor.productos:
                    if pedido not in vendedor.pedidos_activos:
                        vendedor.pedidos_activos.append(pedido)
        return pedido

    def asignar_turno(self, pedido: Pedido):
        for i in range(len(self.pedidos)):
            if self.pedidos[i] == pedido:
                return i + 1
        return -1

    def calcular_congestion(self, vendedor: Vendedor):
        return len(vendedor.pedidos_activos) / 10

    def recomendar_menu(self, usuario: Usuario):
        todos = []
        for v in self.vendedores:
            for p in v.productos:
                todos.append(p)
        return self.recomendador.recomendar(usuario, todos)

    def buscar_usuario(self, nombre: str):
        for u in self.usuarios:
            if u.nombre == nombre:
                return u
        return None

    def buscar_vendedor(self, nombre: str):
        for v in self.vendedores:
            if v.nombre == nombre:
                return v
        return None
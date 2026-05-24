from abc import ABC, abstractmethod

class FoodUError(Exception): pass

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


class Persona(ABC):
    def __init__(self, nombre: str, contrasena: str):
        self.__nombre = nombre
        self.__contrasena = contrasena

    @property
    def nombre(self): return self.__nombre
    @property
    def contrasena(self): return self.__contrasena

    @nombre.setter
    def nombre(self, v):
        if not v or len(v) <= 2: raise ValueError("El nombre debe tener mas de 2 caracteres")
        self.__nombre = v

    @contrasena.setter
    def contrasena(self, v):
        if len(v) < 4: raise ValueError("La contrasena debe tener al menos 4 caracteres")
        self.__contrasena = v

    @abstractmethod
    def __str__(self): pass


class Producto:
    def __init__(self, producto_id, nombre, precio, tiempo_preparacion, disponible, imagen=""):
        if precio < 0: raise ValueError("El precio no puede ser negativo")
        if tiempo_preparacion <= 0: raise ValueError("El tiempo debe ser mayor a 0")
        self.id = producto_id
        self.__nombre = nombre
        self.__precio = precio
        self.__tiempo_preparacion = tiempo_preparacion
        self.disponible = disponible
        self.imagen = imagen

    @property
    def nombre(self): return self.__nombre
    @property
    def precio(self): return self.__precio
    @property
    def tiempo_preparacion(self): return self.__tiempo_preparacion

    @nombre.setter
    def nombre(self, v):
        if not v: raise ValueError("El nombre no puede estar vacio")
        self.__nombre = v
    @precio.setter
    def precio(self, v):
        if v < 0: raise ValueError("Precio negativo")
        self.__precio = v
    @tiempo_preparacion.setter
    def tiempo_preparacion(self, v):
        if v <= 0: raise ValueError("Tiempo debe ser mayor a 0")
        self.__tiempo_preparacion = v

    def actualizar_disponibilidad(self, estado): self.disponible = estado

    def __str__(self):
        return f"[{self.id}] {self.__nombre} - ${self.__precio} | {self.__tiempo_preparacion} min"


class Pedido:
    ESTADOS_VALIDOS = ["pendiente", "en preparacion", "listo", "entregado", "cancelado"]

    def __init__(self, pedido_id, usuario):
        self.id = pedido_id
        self.usuario = usuario
        self.productos = []
        self.__estado = "pendiente"
        self.tiempo_estimado = 0
        self.total = 0.0

    @property
    def estado(self): return self.__estado
    @estado.setter
    def estado(self, v): self.__estado = v

    def calcular_tiempo(self):
        if not self.productos: raise PedidoVacioError()
        self.tiempo_estimado = max(p.tiempo_preparacion for p in self.productos)
        return self.tiempo_estimado

    def calcular_total(self):
        if not self.productos: raise PedidoVacioError()
        self.total = sum(p.precio for p in self.productos)
        return self.total

    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado '{nuevo_estado}' no valido.")
        self.__estado = nuevo_estado

    def __str__(self):
        return f"Pedido #{self.id} | {self.__estado} | Total: ${self.total}"


class Usuario(Persona):
    def __init__(self, usuario_id, nombre, correo, tiempo_disponible, contrasena):
        super().__init__(nombre, contrasena)
        self.id = usuario_id
        self.__correo = correo
        self.tiempo_disponible = tiempo_disponible
        self.historial_pedidos = []

    @property
    def correo(self): return self.__correo
    @correo.setter
    def correo(self, v):
        if "@" not in v: raise ValueError("Correo invalido")
        self.__correo = v

    def realizar_pedido(self, productos):
        if not productos: raise PedidoVacioError()
        pedido = Pedido(len(self.historial_pedidos) + 1, self)
        pedido.productos = productos
        pedido.calcular_tiempo()
        pedido.calcular_total()
        self.historial_pedidos.append(pedido)
        return pedido

    def ver_historial(self): return self.historial_pedidos

    def calificar_vendedor(self, vendedor, puntuacion):
        if not (1 <= puntuacion <= 5): raise PuntuacionInvalidaError(puntuacion)
        vendedor.calificacion = puntuacion if vendedor.calificacion == 0 \
            else (vendedor.calificacion + puntuacion) / 2

    def __str__(self): return f"Usuario: {self.nombre} | Correo: {self.__correo}"


class Vendedor(Persona):
    def __init__(self, nombre, contrasena, logo="", ubicacion=""):
        super().__init__(nombre, contrasena)
        self.productos = []
        self.pedidos_activos = []
        self.calificacion = 0.0
        self.logo = logo          # ← NUEVO: nombre de archivo del logo
        self.ubicacion = ubicacion  # ← NUEVO: ej "Bloque 3 - Edificio Ingeniería"

    def agregar_producto(self, producto):
        if not isinstance(producto, Producto): raise TypeError("Solo objetos Producto")
        self.productos.append(producto)

    def editar_producto(self, producto_id, nuevo_nombre, nuevo_precio, nuevo_tiempo, nueva_disp):
        for p in self.productos:
            if p.id == producto_id:
                p.nombre = nuevo_nombre
                p.precio = nuevo_precio
                p.tiempo_preparacion = nuevo_tiempo
                p.disponible = nueva_disp
                return
        raise ProductoNoEncontradoError(producto_id)

    def eliminar_producto(self, producto_id):
        for p in self.productos:
            if p.id == producto_id:
                self.productos.remove(p)
                return
        raise ProductoNoEncontradoError(producto_id)

    def gestionar_pedidos(self): return self.pedidos_activos

    def __str__(self): return f"Vendedor: {self.nombre} | Calificacion: {self.calificacion}"


class Recomendador:
    def recomendar(self, usuario, todos_productos):
        try:
            disponibles = [p for p in todos_productos if p.disponible]
            if not usuario.historial_pedidos:
                return sorted(disponibles, key=lambda p: p.precio)[:3]
            conteo = {}
            for pedido in usuario.historial_pedidos:
                for p in pedido.productos:
                    conteo[p.id] = conteo.get(p.id, 0) + 1
            return sorted(disponibles, key=lambda p: conteo.get(p.id, 0), reverse=True)[:3]
        except Exception as e:
            print(f"Error recomendaciones: {e}")
            return []


class SistemaFoodU:
    def __init__(self):
        self.usuarios = []
        self.vendedores = []
        self.pedidos = []
        self.recomendador = Recomendador()

    def registrar_usuario(self, usuario):
        try:
            for u in self.usuarios:
                if u.nombre == usuario.nombre: raise UsuarioDuplicadoError("nombre de usuario")
                if u.correo == usuario.correo: raise UsuarioDuplicadoError("correo")
            self.usuarios.append(usuario)
            return "Usuario registrado correctamente"
        except UsuarioDuplicadoError as e: return str(e)

    def registrar_vendedor(self, vendedor):
        try:
            for v in self.vendedores:
                if v.nombre == vendedor.nombre: raise VendedorDuplicadoError(vendedor.nombre)
            self.vendedores.append(vendedor)
            return "Vendedor registrado correctamente"
        except VendedorDuplicadoError as e: return str(e)

    def crear_pedido(self, usuario, productos):
        if not productos: raise PedidoVacioError()
        pedido = usuario.realizar_pedido(productos)
        self.pedidos.append(pedido)
        for v in self.vendedores:
            for p in productos:
                if p in v.productos and pedido not in v.pedidos_activos:
                    v.pedidos_activos.append(pedido)
        return pedido

    def asignar_turno(self, pedido):
        for i, p in enumerate(self.pedidos):
            if p == pedido: return i + 1
        return -1

    def calcular_congestion(self, vendedor): return len(vendedor.pedidos_activos) / 10

    def recomendar_menu(self, usuario):
        todos = [p for v in self.vendedores for p in v.productos]
        return self.recomendador.recomendar(usuario, todos)

    def buscar_usuario(self, nombre):
        for u in self.usuarios:
            if u.nombre == nombre: return u
        return None

    def buscar_vendedor(self, nombre):
        for v in self.vendedores:
            if v.nombre == nombre: return v
        return None
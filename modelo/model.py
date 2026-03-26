class  Producto:
    def __init__(self, producto_id: int, nombre: str, precio: float, tiempo_preparacion: int, disponible: bool):
        self.id: int = producto_id
        self.nombre: str = nombre
        self.precio: float = precio
        self.tiempo_preparacion: int = tiempo_preparacion
        self.disponible: bool = disponible

    def actualizar_disponibilidad(self, estado: bool)->str | None:
        self.disponible = estado

    def __str__(self):
        if self.disponible:
            estado = "Disponible"
        else:
            estado = "No disponible"
        return f"[{self.id}] {self.nombre} - ${self.precio} | {self.tiempo_preparacion} min | {estado}"

class Pedido:
    def __init__(self, pedido_id: int, usuario: "Usuario"):
        self.id: int = pedido_id
        self.usuario: Usuario = usuario
        self.productos: list[Producto] = []
        self.estado: str = "pendiente"
        self.tiempo_estimado: int = 0
        self.total: float = 0.0

    def calcular_tiempo(self):
        mayor = 0
        for p in self.productos:
            if p.tiempo_preparacion > mayor:
                mayor = p.tiempo_preparacion
        self.tiempo_estimado = mayor
        return self.tiempo_estimado

    def calcular_total(self):
        suma = 0
        for p in self.productos:
            suma = suma + p.precio
        self.total = suma
        return self.total

    def cambiar_estado(self, nuevo_estado: str):
        self.estado = nuevo_estado

    def __str__(self):
        texto = f"Pedido #{self.id} | Estado: {self.estado}\n"
        texto = texto + f"  Usuario: {self.usuario.nombre}\n"
        texto = texto + f"  Productos:\n"
        for p in self.productos:
            texto = texto + f"    - {p.nombre} ${p.precio}\n"
        texto = texto + f"  Tiempo estimado: {self.tiempo_estimado} min\n"
        texto = texto + f"  Total: ${self.total}"
        return texto

class Usuario:
    def __init__(self, usuario_id: int, nombre: str, correo: str, tiempo_disponible: int):
        self.id: int = usuario_id
        self.nombre: str = nombre
        self.correo: str = correo
        self.historial_pedidos: list[Pedido] = []

    def realizar_pedido(self, productos: list):
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
        if puntuacion >= 1 and puntuacion <= 5:
            if vendedor.calificacion == 0:
                vendedor.calificacion = puntuacion
            else:
                vendedor.calificacion = (vendedor.calificacion + puntuacion) / 2
            print("Calificacion registrada correctamente")
        else:
            print("La calificacion debe ser entre 1 y 5")

    def __str__(self):
        return f"Usuario: {self.nombre} | Correo: {self.correo}"

class Vendedor:
    def __init__(self, nombre: str):
        self.nombre: str = nombre
        self.productos: list[Producto] = []
        self.pedidos_activos: list = []
        self.calificacion: float = 0.0


    def agregar_producto(self, producto: Producto):
        self.productos.append(producto)
        print("Producto agregado correctamente")

    def editar_producto(self, producto_id: int, nuevo_nombre: str, nuevo_precio: float, nuevo_tiempo: int,
                       nueva_disponibilidad: bool):
        for p in self.productos:
            if p.id == producto_id:
                p.nombre = nuevo_nombre
                p.precio = nuevo_precio
                p.tiempo_preparacion = nuevo_tiempo
                p.disponible = nueva_disponibilidad
                print("Producto editado correctamente")
                return
        print("No se encontro un producto con ese ID")

    def eliminar_producto(self, producto_id: int):
        for p in self.productos:
            if p.id == producto_id:
                self.productos.remove(p)
                print("Producto eliminado correctamente")
                return
        print("No se encontro un producto con ese ID")

    def gestionar_pedidos(self):
        return self.pedidos_activos

    def __str__(self):
        return f"Vendedor: {self.nombre} | Calificacion: {self.calificacion}"


class Recomendador:
    def recomendar(self, usuario: Usuario, todos_productos: list):
        if len(usuario.historial_pedidos) == 0:
            disponibles = []
            for p in todos_productos:
                if p.disponible:
                    disponibles.append(p)

            for i in range(len(disponibles)):
                for j in range(i + 1, len(disponibles)):
                    if disponibles[i].precio > disponibles[j].precio:
                        temp = disponibles[i]
                        disponibles[i] = disponibles[j]
                        disponibles[j] = temp

            return disponibles[:3]

        conteo = {}
        for pedido in usuario.historial_pedidos:
            for producto in pedido.productos:
                if producto.id in conteo:
                    conteo[producto.id] = conteo[producto.id] + 1
                else:
                    conteo[producto.id] = 1
        disponibles = []
        for p in todos_productos:
            if p.disponible:
                disponibles.append(p)

        for i in range(len(disponibles)):
            for j in range(i + 1, len(disponibles)):
                veces_i = 0
                veces_j = 0
                if disponibles[i].id in conteo:
                    veces_i = conteo[disponibles[i].id]
                if disponibles[j].id in conteo:
                    veces_j = conteo[disponibles[j].id]
                if veces_i < veces_j:
                    temp = disponibles[i]
                    disponibles[i] = disponibles[j]
                    disponibles[j] = temp

        return disponibles[:3]


class SistemaFoodU:
    def __init__(self):
        self.usuarios: list = []
        self.vendedores: list= []
        self.pedidos: list = []
        self.recomendador = Recomendador()

    def registrar_usuario(self, usuario: Usuario):
        for u in self.usuarios:
            if u.nombre == usuario.nombre:
                return "Error: ese nombre de usuario ya existe"
            if u.correo == usuario.correo:
                return "Error: ese correo ya esta registrado"
        self.usuarios.append(usuario)
        return "Usuario registrado correctamente"

    def registrar_vendedor(self, vendedor: Vendedor):
        for v in self.vendedores:
            if v.nombre == vendedor.nombre:
                return "Error: ese nombre de vendedor ya existe"
        self.vendedores.append(vendedor)
        return "Vendedor registrado correctamente"

    def crear_pedido(self, usuario: Usuario, productos: list):
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

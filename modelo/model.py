from mimetypes import init
class  Producto:
    def __init__(self,nombre:str,precio:float,tiempo_preparacion:int,disponible:bool):
        self.nombre:str =nombre
        self.precio:float = precio
        self.tiempo_preparacion:int = tiempo_preparacion
        self.disponible: bool = False

def actualizar_disponibilidad(self, estado: bool):
    self.disponible = estado

    def _str_(self):
        if self.disponible:
            estado = "Disponible"
        else:
            estado = "No disponible"
        return f"[{self.id}] {self.nombre} - ${self.precio} | {self.tiempo_preparacion} min | {estado}"


class Pedido:
    def __init__(self, id: int, usuario: "Usuario", estado: str, tiempo_estimado: int, total: float):
        self.id: int = id
        self.usuario: Usuario = usuario
        self.productos: list = []
        self.estado: str = estado
        self.tiempo_estimado: int = tiempo_estimado
        self.total: float = total




class Usuario:
    def __init__(self, id: int, nombre: str, correo: str, tiempo_disponible: int):
        self.id: int = id
        self.nombre: str = nombre
        self.correo: str = correo
        self.historial_pedidos: list[Pedido] = []

    def realizar_pedido(self, productos: list):
        id_nuevo = len(self.historial_pedidos) + 1
        pedido = Pedido(id_nuevo, self)
        pedido.productos = productos
        pedido.calcularTiempo()
        pedido.calcularTotal()
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

    def _str_(self):
        return f"Usuario: {self.nombre} | Correo: {self.correo}"






class Vendedor:
    def __init__(self,nombre:str,calificaciones:float):

        self.nombre: str = nombre
        self.productos: list[Producto] = []
        self.pedidos_activos: list[Pedido] = []
        self.calificacion: float = calificaciones

    def crearProducto(self, nombre:str, precio: float, tiempo_preparacion: int ,disponible: bool):
        nuevo_producto =  Producto(nombre, precio, tiempo_preparacion, disponible)
        self.productos.append(nuevo_producto)
        return nuevo_producto



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
        self.usuarios = []
        self.vendedores = []
        self.pedidos = []
        self.recomendador = Recomendador()

    def registrarUsuario(self, usuario: Usuario):
        for u in self.usuarios:
            if u.nombre == usuario.nombre:
                return "Error: ese nombre de usuario ya existe"
            if u.correo == usuario.correo:
                return "Error: ese correo ya esta registrado"
        self.usuarios.append(usuario)
        return "Usuario registrado correctamente"

    def registrar_vendedor(self,vendedor:Vendedor)->str:
        for i in self.vendedor:
            if vendedor.nombre == i.nombre:
                return "!Error Este nombre ve vendedor ya Existre en nuestro sistema"
        self.vendedor.append(vendedor)





    def CrearPedido(self,usuario:Usuario,productos):
        pass




















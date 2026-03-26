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

    def realizarPedido(self, productos: list):
        id_nuevo = len(self.historial_pedidos) + 1
        pedido = Pedido(id_nuevo, self)
        pedido.productos = productos
        pedido.calcularTiempo()
        pedido.calcularTotal()
        self.historial_pedidos.append(pedido)
        return pedido

    def verHistorial(self):
        return self.historial_pedidos

    def calificarVendedor(self, vendedor: "Vendedor", puntuacion: int):
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







class SistemaFoodU:
    def __init__(self):
        self.usuarios: list[Usuario] = []
        self.vendedor: list [Vendedor] = []
        self.pedidos: list [Pedido] = []


    def registrar_usuario(self,usuario:Usuario)->str:
        for i in self.usuarios:
            if usuario.nombre == i.nombre:
                return "!Error Este nombre de usuario ya Existe en nuestro sistema"


        self.usuarios.append(usuario)



    def registrar_vendedor(self,vendedor:Vendedor)->str:
        for i in self.vendedor:
            if vendedor.nombre == i.nombre:
                return "!Error Este nombre ve vendedor ya Existre en nuestro sistema"
        self.vendedor.append(vendedor)





    def CrearPedido(self,usuario:Usuario,productos):




















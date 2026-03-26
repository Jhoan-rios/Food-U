from mimetypes import init
class  Producto:
    def __init__(self,nombre:str,precio:float,tiempo_preparacion:int,disponible:bool):
        self.nombre:str =nombre
        self.precio:float = precio
        self.tiempo_preparacion:int = tiempo_preparacion
        self.disponibile:bool= disponible







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

    def realizarPedido(self,produtos:list[Producto])->Pedido:
        pass








class Vendedor:
    def __init__(self,nombre:str,calificaciones:float):


        self.nombre: str = nombre
        self.productos: list[Producto] = []
        self.pedidos_activos: list[Pedido] = []
        self.calificacion: float = calificaciones










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



















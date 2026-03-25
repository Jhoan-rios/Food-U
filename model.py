class Usuario:
    def __init__(self,id:int,nombre:str,correo:str,tiempo_disponible:int):
        self.id:int=id
        self.nombre:str=nombre
        self.correo:str=correo
        self.historial_pedidos:list= []
        self.tiempo_disponible:int=tiempo_disponible





class Vendedor:
    def __init__(self,nombre:str,calificaciones:float):


        self.nombre: str = nombre
        self.productos: list[Producto] = []
        self.pedidos_activos: list = []
        self.calificacion: float = calificaciones



class  Producto:
    def __init__(self,int:int,nombre:str,precio:float,tiempo_preparacion:int,disponible:bool):

        self.int:int = int
        self.nombre:str =nombre
        self.precio:float = precio
        self.tiempo_preparacion:int = tiempo_preparacion
        self.disponibile:bool=disponible







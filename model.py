class Usuario:
    def __init__(self,id:int,nombre:str,correo:str,tiempo_disponible:int):
        self.id:int=id
        self.nombre:str=nombre
        self.correo:str=correo
        self.historial_pedidos:list= []
        self.tiempo_disponible:int=tiempo_disponible



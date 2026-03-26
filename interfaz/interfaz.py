
from modelo.model import Usuario
from modelo.model import SistemaFoodU
from modelo.model import Vendedor


class Interfaz:
    sistema =SistemaFoodU()

    def datos_usuarios(self):
        print("Ingrese los siguientes datos")

        id= input("ID:")
        nombre=input("Nombre:")
        correo = input("Correo:")

        usuario = Usuario(id,nombre,correo)



        SistemaFoodU.registrar_usuario(usuario)


    def datos_vendedor(self):
        print("Ingrese los siguientes datos")
        nombre = input("Nombre:")
        vendedor= Vendedor(nombre)
        SistemaFoodU.registrar_vendedor(vendedor)


    def mostrar_vendedores(self):
        print()
        for i in self.sistema.vendedor:
            print(i)















    def show_menu(self):
        print("BIENVENIDO A EL SISTEMA FOOTU-UNIVERSIDAD DE MEDELLIN\n")

        opcion = input("SELECCIONE EL TIPO DE USUARIO QUE ERES: U) USUARIO V) VENDEDOR")

        if opcion == "U":

            while True:
                print("1)Registrar Usuario")
                print("2)Crear Pedido")

                opcion = int(input("ingrese alguna opcion:"))

                if opcion == 1:
                    self.datos_usuarios()







        elif opcion == "V":

            while True:
                print("1)Resgistrar Vendedor")
                print("2)Gistion De Pedidos")

                opcion = int(input("ingrese alguna opcion:"))

                if opcion == 1:
                    self.datos_vendedor()

                if opcion == 2:

                    self.mostrar_vendedores()












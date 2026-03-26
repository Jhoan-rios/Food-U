from modelo.model import Usuario
from modelo.model import Vendedor
from modelo.model import Producto
from modelo.model import SistemaFoodU


class Interfaz:
    class Interfaz:
        def __init__(self):
            self.sistema = SistemaFoodU()
            self.id_usuario = 1
            self.id_producto = 1

    def registrar_usuario(self):
        print("\n-- REGISTRAR USUARIO --")
        nombre = input("Nombre: ")
        correo = input("Correo: ")
        tiempo = input("Tiempo disponible en minutos (ejemplo: 60): ")

        usuario = Usuario(self.id_usuario, nombre, correo, int(tiempo))
        resultado = self.sistema.registrarUsuario(usuario)
        print(resultado)

        if resultado == "Usuario registrado correctamente":
            self.id_usuario = self.id_usuario + 1

        input("\nPresione ENTER para continuar...")

    def crear_pedido(self):
        print("\n-- CREAR PEDIDO --")

        if len(self.sistema.usuarios) == 0:
            print("No hay usuarios registrados.")
            input("\nPresione ENTER para continuar...")
            return

        if len(self.sistema.vendedores) == 0:
            print("No hay vendedores registrados.")
            input("\nPresione ENTER para continuar...")
            return

        nombre = input("Ingrese su nombre de usuario: ")
        usuario = self.sistema.buscarUsuario(nombre)

        if usuario == None:
            print("Usuario no encontrado.")
            input("\nPresione ENTER para continuar...")
            return














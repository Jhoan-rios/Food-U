from modelo.model import Usuario
from modelo.model import Vendedor
from modelo.model import Producto
from modelo.model import SistemaFoodU


class Interfaz:
    def __init__(self):
        self.sistema = SistemaFoodU()
        self.id_usuario: int = 1
        self.id_producto: int = 1

    def registrar_usuario(self):
        print("\n-- REGISTRAR USUARIO --")
        nombre = input("Nombre: ")
        correo = input("Correo: ")
        tiempo = input("Tiempo disponible en minutos (ejemplo: 60): ")

        usuario = Usuario(self.id_usuario, nombre, correo, int(tiempo))
        resultado = self.sistema.registrar_usuario(usuario)
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
        usuario = self.sistema.buscar_usuario(nombre)

        if usuario == None:
            print("Usuario no encontrado.")
            input("\nPresione ENTER para continuar...")
            return

        todos_disponibles = []
        for v in self.sistema.vendedores:
            for p in v.productos:
                if p.disponible:
                    todos_disponibles.append(p)

        if len(todos_disponibles) == 0:
            print("No hay productos disponibles en este momento.")
            input("\nPresione ENTER para continuar...")
            return

        print("\nProductos disponibles:")
        for p in todos_disponibles:
            print(p)

        print("\nIngrese los IDs de los productos que desea pedir.")
        print("Separe los IDs con coma. Ejemplo: 1,2,3")
        ids_texto = input("IDs: ")

        ids_lista = ids_texto.split(",")
        seleccionados = []

        for id_str in ids_lista:
            id_str = id_str.strip()
            if id_str.isdigit():
                id_num = int(id_str)
                for p in todos_disponibles:
                    if p.id == id_num:
                        seleccionados.append(p)

        if len(seleccionados) == 0:
            print("No se selecciono ningun producto valido.")
            input("\nPresione ENTER para continuar...")
            return

        pedido = self.sistema.crear_pedido(usuario, seleccionados)
        turno = self.sistema.asignar_turno(pedido)

        print("\nPedido creado exitosamente:")
        print(pedido)
        print(f"\nSu turno en la cola es el numero: {turno}")

        recomendados = self.sistema.recomendar_menu(usuario)
        if len(recomendados) > 0:
            print("\nTambien te puede interesar:")
            for r in recomendados:
                print(" -", r)

        input("\nPresione ENTER para continuar...")

    def ver_historial(self):
        print("\n-- HISTORIAL DE PEDIDOS --")
        nombre = input("Ingrese su nombre de usuario: ")
        usuario = self.sistema.buscar_usuario(nombre)

        if usuario == None:
            print("Usuario no encontrado.")
            input("\nPresione ENTER para continuar...")
            return

        historial = usuario.ver_historial()

        if len(historial) == 0:
            print(f"{usuario.nombre} no tiene pedidos registrados.")
        else:
            print(f"\nHistorial de {usuario.nombre}:")
            for pedido in historial:
                print("\n" + str(pedido))

        input("\nPresione ENTER para continuar...")

    def calificar_vendedor(self):
        print("\n-- CALIFICAR VENDEDOR --")
        nombre_usuario = input("Su nombre de usuario: ")
        usuario = self.sistema.buscar_usuario(nombre_usuario)

        if usuario == None:
            print("Usuario no encontrado.")
            input("\nPresione ENTER para continuar...")
            return

        nombre_vendedor = input("Nombre del vendedor a calificar: ")
        vendedor = self.sistema.buscar_vendedor(nombre_vendedor)

        if vendedor == None:
            print("Vendedor no encontrado.")
            input("\nPresione ENTER para continuar...")
            return

        puntuacion = input("Puntuacion del 1 al 5: ")

        if puntuacion.isdigit():
            usuario.calificar_vendedor(vendedor, int(puntuacion))
        else:
            print("Puntuacion invalida.")

        input("\nPresione ENTER para continuar...")

    def ver_recomendaciones(self):
        print("\n-- RECOMENDACIONES --")
        nombre = input("Ingrese su nombre de usuario: ")
        usuario = self.sistema.buscar_usuario(nombre)

        if usuario == None:
            print("Usuario no encontrado.")
            input("\nPresione ENTER para continuar...")
            return

        recomendados = self.sistema.recomendar_menu(usuario)

        if len(recomendados) == 0:
            print("No hay productos disponibles para recomendar.")
        else:
            print(f"\nRecomendaciones para {usuario.nombre}:")
            for p in recomendados:
                print(" -", p)

        input("\nPresione ENTER para continuar...")

    def registrar_vendedor(self):
        print("\n-- REGISTRAR VENDEDOR --")
        nombre = input("Nombre del vendedor: ")
        vendedor = Vendedor(nombre)
        resultado = self.sistema.registrar_vendedor(vendedor)
        print(resultado)
        input("\nPresione ENTER para continuar...")

    def agregar_producto(self):
        print("\n-- AGREGAR PRODUCTO --")
        nombre_vendedor = input("Nombre del vendedor: ")
        vendedor = self.sistema.buscar_vendedor(nombre_vendedor)

        if vendedor == None:
            print("Vendedor no encontrado.")
            input("\nPresione ENTER para continuar...")
            return

        nombre = input("Nombre del producto: ")
        precio = float(input("Precio: "))
        tiempo = int(input("Tiempo de preparacion en minutos: "))
        disp = input("Esta disponible? (s/n): ")

        if disp == "s":
            disponible = True
        else:
            disponible = False

        producto = Producto(self.id_producto, nombre, precio, tiempo, disponible)
        vendedor.agregar_producto(producto)
        self.id_producto = self.id_producto + 1

        input("\nPresione ENTER para continuar...")

    def editar_producto(self):
        print("\n-- EDITAR PRODUCTO --")
        nombre_vendedor = input("Nombre del vendedor: ")
        vendedor = self.sistema.buscar_vendedor(nombre_vendedor)

        if vendedor == None:
            print("Vendedor no encontrado.")
            input("\nPresione ENTER para continuar...")
            return

        if len(vendedor.productos) == 0:
            print("Este vendedor no tiene productos.")
            input("\nPresione ENTER para continuar...")
            return

        print("\nProductos del vendedor:")
        for p in vendedor.productos:
            print(p)

        id_str = input("\nID del producto a editar: ")
        if id_str.isdigit() == False:
            print("ID invalido.")
            input("\nPresione ENTER para continuar...")
            return

        nuevo_nombre = input("Nuevo nombre: ")
        nuevo_precio = float(input("Nuevo precio: "))
        nuevo_tiempo = int(input("Nuevo tiempo de preparacion: "))
        disp = input("Esta disponible? (s/n): ")

        if disp == "s":
            nueva_disp = True
        else:
            nueva_disp = False

        vendedor.editar_producto(int(id_str), nuevo_nombre, nuevo_precio, nuevo_tiempo, nueva_disp)
        input("\nPresione ENTER para continuar...")

    def eliminar_producto(self):
        print("\n-- ELIMINAR PRODUCTO --")
        nombre_vendedor = input("Nombre del vendedor: ")
        vendedor = self.sistema.buscar_vendedor(nombre_vendedor)

        if vendedor == None:
            print("Vendedor no encontrado.")
            input("\nPresione ENTER para continuar...")
            return

        if len(vendedor.productos) == 0:
            print("Este vendedor no tiene productos.")
            input("\nPresione ENTER para continuar...")
            return

        print("\nProductos del vendedor:")
        for p in vendedor.productos:
            print(p)

        id_str = input("\nID del producto a eliminar: ")

        if id_str.isdigit():
            vendedor.eliminar_producto(int(id_str))
        else:
            print("ID invalido.")

        input("\nPresione ENTER para continuar...")

    def gestionar_pedidos(self):
        print("\n-- GESTIONAR PEDIDOS --")
        nombre_vendedor = input("Nombre del vendedor: ")
        vendedor = self.sistema.buscar_vendedor(nombre_vendedor)

        if vendedor == None:
            print("Vendedor no encontrado.")
            input("\nPresione ENTER para continuar...")
            return

        pedidos = vendedor.gestionar_pedidos()

        if len(pedidos) == 0:
            print("No hay pedidos activos.")
            input("\nPresione ENTER para continuar...")
            return

        congestion = self.sistema.calcular_congestion(vendedor)
        print(f"Nivel de congestion: {congestion * 100}%")

        print(f"\nPedidos activos de {vendedor.nombre}:")
        for pedido in pedidos:
            print("\n" + str(pedido))

        id_str = input("\nID del pedido a cambiar de estado (Enter para omitir): ")

        if id_str.isdigit():
            id_num = int(id_str)
            pedido_encontrado = None
            for pedido in pedidos:
                if pedido.id == id_num:
                    pedido_encontrado = pedido

            if pedido_encontrado == None:
                print("Pedido no encontrado.")
            else:
                print("Estados posibles: pendiente | en preparacion | listo | entregado | cancelado")
                nuevo_estado = input("Nuevo estado: ")
                pedido_encontrado.cambiar_estado(nuevo_estado)
                print("Estado actualizado.")

        input("\nPresione ENTER para continuar...")

    def mostrar_vendedores(self):
        print("\n-- VENDEDORES REGISTRADOS --")
        if len(self.sistema.vendedores) == 0:
            print("No hay vendedores registrados.")
        else:
            for v in self.sistema.vendedores:
                print("\n" + str(v))
                if len(v.productos) == 0:
                    print("  Sin productos en el menu")
                else:
                    for p in v.productos:
                        print("  ", p)
        input("\nPresione ENTER para continuar...")

    def menu_usuario(self):
        while True:
            print("\n========== MENU USUARIO ==========")
            print("1) Registrar usuario")
            print("2) Crear pedido")
            print("3) Ver historial de pedidos")
            print("4) Calificar vendedor")
            print("5) Ver recomendaciones")
            print("0) Volver")

            opcion = input("\nSeleccione una opcion: ")

            if opcion == "1":
                self.registrar_usuario()
            elif opcion == "2":
                self.crear_pedido()
            elif opcion == "3":
                self.ver_historial()
            elif opcion == "4":
                self.calificar_vendedor()
            elif opcion == "5":
                self.ver_recomendaciones()
            elif opcion == "0":
                break
            else:
                print("Opcion invalida.")

    def menu_vendedor(self):
        while True:
            print("\n========== MENU VENDEDOR ==========")
            print("1) Registrar vendedor")
            print("2) Agregar producto")
            print("3) Editar producto")
            print("4) Eliminar producto")
            print("5) Gestionar pedidos")
            print("6) Ver todos los vendedores")
            print("0) Volver")

            opcion = input("\nSeleccione una opcion: ")

            if opcion == "1":
                self.registrar_vendedor()
            elif opcion == "2":
                self.agregar_producto()
            elif opcion == "3":
                self.editar_producto()
            elif opcion == "4":
                self.eliminar_producto()
            elif opcion == "5":
                self.gestionar_pedidos()
            elif opcion == "6":
                self.mostrar_vendedores()
            elif opcion == "0":
                break
            else:
                print("Opcion invalida.")

    def show_menu(self):
        while True:
            print("\n========================================")
            print("  BIENVENIDO A FOODU - UDEM MEDELLIN")
            print("========================================")
            print("U) Soy Usuario")
            print("V) Soy Vendedor")
            print("Q) Salir")

            opcion = input("\nSeleccione su tipo: ").upper()

            if opcion == "U":
                self.menu_usuario()
            elif opcion == "V":
                self.menu_vendedor()
            elif opcion == "Q":
                print("\nHasta luego!")
                break
            else:
                print("Opcion invalida.")
















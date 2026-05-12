import re
from modelo.model import Usuario
from modelo.model import Vendedor
from modelo.model import Producto
from modelo.model import SistemaFoodU
from modelo.persistencia import guardar_datos, cargar_datos


class Interfaz:
    def __init__(self):
        self.sistema = SistemaFoodU()
        self.id_usuario, self.id_producto = cargar_datos(self.sistema)
        self.usuario_actual = None
        self.vendedor_actual = None

    # ─────────────────────────────────────────
    # LOGIN
    # ─────────────────────────────────────────

    def login_usuario(self):
        print("\n-- INICIAR SESIÓN USUARIO --")
        nombre = input("Nombre de usuario: ").strip()
        contrasena = input("Contraseña: ").strip()

        usuario = self.sistema.buscar_usuario(nombre)

        if usuario is None or usuario.contrasena != contrasena:
            print("Nombre o contraseña incorrectos.")
            input("\nPresione ENTER para continuar...")
            return False

        self.usuario_actual = usuario
        print(f"\nBienvenido, {usuario.nombre}!")
        input("\nPresione ENTER para continuar...")
        return True

    def login_vendedor(self):
        print("\n-- INICIAR SESIÓN VENDEDOR --")
        nombre = input("Nombre del vendedor: ").strip()
        contrasena = input("Contraseña: ").strip()

        vendedor = self.sistema.buscar_vendedor(nombre)

        if vendedor is None or vendedor.contrasena != contrasena:
            print("Nombre o contraseña incorrectos.")
            input("\nPresione ENTER para continuar...")
            return False

        self.vendedor_actual = vendedor
        print(f"\nBienvenido, {vendedor.nombre}!")
        input("\nPresione ENTER para continuar...")
        return True

    # ─────────────────────────────────────────
    # ACCIONES DE USUARIO
    # ─────────────────────────────────────────

    def registrar_usuario(self):
        print("\n-- REGISTRAR USUARIO --")
        while True:
            nombre = input("Ingrese su nombre: ").strip()
            if not nombre:
                print("Debe ingresar el nombre.")
            elif len(nombre) <= 2:
                print(f"El nombre '{nombre}' no es válido, debe ser más largo.")
            else:
                break

        while True:
            correo = input("Ingrese su correo: ").strip()
            if not correo:
                print("Debe ingresar el correo.")
                continue
            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo):
                print("Debe ingresar un correo válido (ej: usuario@gmail.com).")
                continue
            break

        while True:
            tiempo = input("Tiempo disponible en minutos (ejemplo: 60): ").strip()
            if not tiempo or not tiempo.isdigit():
                print("Debe ingresar un número entero.")
            else:
                break

        while True:
            contrasena = input("Ingrese una contraseña (mínimo 4 caracteres): ").strip()
            if len(contrasena) < 4:
                print("La contraseña debe tener al menos 4 caracteres.")
            else:
                break

        usuario = Usuario(self.id_usuario, nombre, correo, int(tiempo), contrasena)
        resultado = self.sistema.registrar_usuario(usuario)
        print(resultado)

        if resultado == "Usuario registrado correctamente":
            self.id_usuario = self.id_usuario + 1
            guardar_datos(self.sistema, self.id_usuario, self.id_producto)

        input("\nPresione ENTER para continuar...")

    def crear_pedido(self):
        print("\n-- CREAR PEDIDO --")

        if len(self.sistema.vendedores) == 0:
            print("No hay vendedores registrados.")
            input("\nPresione ENTER para continuar...")
            return

        usuario = self.usuario_actual

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

        guardar_datos(self.sistema, self.id_usuario, self.id_producto)
        input("\nPresione ENTER para continuar...")

    def ver_historial(self):
        print("\n-- HISTORIAL DE PEDIDOS --")
        usuario = self.usuario_actual
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
        usuario = self.usuario_actual

        nombre_vendedor = input("Nombre del vendedor a calificar: ")
        vendedor = self.sistema.buscar_vendedor(nombre_vendedor)

        if vendedor is None:
            print("Vendedor no encontrado.")
            input("\nPresione ENTER para continuar...")
            return

        puntuacion = input("Puntuacion del 1 al 5: ")

        if puntuacion.isdigit():
            usuario.calificar_vendedor(vendedor, int(puntuacion))
            guardar_datos(self.sistema, self.id_usuario, self.id_producto)
        else:
            print("Puntuacion invalida.")

        input("\nPresione ENTER para continuar...")

    def ver_recomendaciones(self):
        print("\n-- RECOMENDACIONES --")
        usuario = self.usuario_actual
        recomendados = self.sistema.recomendar_menu(usuario)

        if len(recomendados) == 0:
            print("No hay productos disponibles para recomendar.")
        else:
            print(f"\nRecomendaciones para {usuario.nombre}:")
            for p in recomendados:
                print(" -", p)

        input("\nPresione ENTER para continuar...")

    # ─────────────────────────────────────────
    # ACCIONES DE VENDEDOR
    # ─────────────────────────────────────────

    def registrar_vendedor(self):
        print("\n-- REGISTRAR VENDEDOR --")
        while True:
            nombre = input("Ingrese el nombre del vendedor: ").strip()
            if not nombre:
                print("Debe ingresar un nombre para registrar.")
            elif len(nombre) <= 2:
                print(f"El nombre '{nombre}' no es valido, debe ser más largo.")
            else:
                break

        while True:
            contrasena = input("Ingrese una contraseña (mínimo 4 caracteres): ").strip()
            if len(contrasena) < 4:
                print("La contraseña debe tener al menos 4 caracteres.")
            else:
                break

        vendedor = Vendedor(nombre, contrasena)
        resultado = self.sistema.registrar_vendedor(vendedor)
        print(resultado)

        if resultado == "Vendedor registrado correctamente":
            guardar_datos(self.sistema, self.id_usuario, self.id_producto)

        input("\nPresione ENTER para continuar...")

    def agregar_producto(self):
        print("\n-- AGREGAR PRODUCTO --")
        vendedor = self.vendedor_actual

        nombre = input("Nombre del producto: ")
        precio = float(input("Precio: "))
        tiempo = int(input("Tiempo de preparacion en minutos: "))
        disp = input("Esta disponible? (s/n): ")

        disponible = True if disp == "s" else False

        producto = Producto(self.id_producto, nombre, precio, tiempo, disponible)
        vendedor.agregar_producto(producto)
        self.id_producto = self.id_producto + 1
        guardar_datos(self.sistema, self.id_usuario, self.id_producto)

        input("\nPresione ENTER para continuar...")

    def editar_producto(self):
        print("\n-- EDITAR PRODUCTO --")
        vendedor = self.vendedor_actual

        if len(vendedor.productos) == 0:
            print("No tienes productos registrados.")
            input("\nPresione ENTER para continuar...")
            return

        print("\nTus productos:")
        for p in vendedor.productos:
            print(p)

        id_str = input("\nID del producto a editar: ")
        if not id_str.isdigit():
            print("ID invalido.")
            input("\nPresione ENTER para continuar...")
            return

        nuevo_nombre = input("Nuevo nombre: ")
        nuevo_precio = float(input("Nuevo precio: "))
        nuevo_tiempo = int(input("Nuevo tiempo de preparacion: "))
        disp = input("Esta disponible? (s/n): ")

        nueva_disp = True if disp == "s" else False

        vendedor.editar_producto(int(id_str), nuevo_nombre, nuevo_precio, nuevo_tiempo, nueva_disp)
        guardar_datos(self.sistema, self.id_usuario, self.id_producto)

        input("\nPresione ENTER para continuar...")

    def eliminar_producto(self):
        print("\n-- ELIMINAR PRODUCTO --")
        vendedor = self.vendedor_actual

        if len(vendedor.productos) == 0:
            print("No tienes productos registrados.")
            input("\nPresione ENTER para continuar...")
            return

        print("\nTus productos:")
        for p in vendedor.productos:
            print(p)

        id_str = input("\nID del producto a eliminar: ")

        if id_str.isdigit():
            vendedor.eliminar_producto(int(id_str))
            guardar_datos(self.sistema, self.id_usuario, self.id_producto)
        else:
            print("ID invalido.")

        input("\nPresione ENTER para continuar...")

    def gestionar_pedidos(self):
        print("\n-- GESTIONAR PEDIDOS --")
        vendedor = self.vendedor_actual
        pedidos = vendedor.gestionar_pedidos()

        if len(pedidos) == 0:
            print("No tienes pedidos activos.")
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

            if pedido_encontrado is None:
                print("Pedido no encontrado.")
            else:
                print("Estados posibles: pendiente | en preparacion | listo | entregado | cancelado")
                nuevo_estado = input("Nuevo estado: ")
                pedido_encontrado.cambiar_estado(nuevo_estado)
                print("Estado actualizado.")

        input("\nPresione ENTER para continuar...")

    def mostrar_mi_menu(self):
        print("\n-- MI MENÚ --")
        vendedor = self.vendedor_actual
        print(f"\n{str(vendedor)}")
        if len(vendedor.productos) == 0:
            print("  Sin productos registrados.")
        else:
            for p in vendedor.productos:
                print("  ", p)
        input("\nPresione ENTER para continuar...")

    # ─────────────────────────────────────────
    # MENÚS
    # ─────────────────────────────────────────

    def menu_usuario(self):
        while True:
            # Sin sesión: solo registro y login
            if self.usuario_actual is None:
                print("\n========== MENU USUARIO ==========")
                print("1) Registrar usuario")
                print("2) Iniciar sesión")
                print("0) Volver")

                opcion = input("\nSeleccione una opcion: ")

                if opcion == "1":
                    self.registrar_usuario()
                elif opcion == "2":
                    self.login_usuario()
                elif opcion == "0":
                    break
                else:
                    print("Opcion invalida.")

            # Con sesión activa: menú completo
            else:
                print(f"\n===== MENU USUARIO ({self.usuario_actual.nombre}) =====")
                print("1) Crear pedido")
                print("2) Ver historial de pedidos")
                print("3) Calificar vendedor")
                print("4) Ver recomendaciones")
                print("0) Cerrar sesión y volver")

                opcion = input("\nSeleccione una opcion: ")

                if opcion == "1":
                    self.crear_pedido()
                elif opcion == "2":
                    self.ver_historial()
                elif opcion == "3":
                    self.calificar_vendedor()
                elif opcion == "4":
                    self.ver_recomendaciones()
                elif opcion == "0":
                    self.usuario_actual = None
                    print("Sesión cerrada.")
                    break
                else:
                    print("Opcion invalida.")

    def menu_vendedor(self):
        while True:
            # Sin sesión: solo registro y login
            if self.vendedor_actual is None:
                print("\n========== MENU VENDEDOR ==========")
                print("1) Registrar vendedor")
                print("2) Iniciar sesión")
                print("0) Volver")

                opcion = input("\nSeleccione una opcion: ")

                if opcion == "1":
                    self.registrar_vendedor()
                elif opcion == "2":
                    self.login_vendedor()
                elif opcion == "0":
                    break
                else:
                    print("Opcion invalida.")

            # Con sesión activa: menú completo
            else:
                print(f"\n===== MENU VENDEDOR ({self.vendedor_actual.nombre}) =====")
                print("1) Agregar producto")
                print("2) Editar producto")
                print("3) Eliminar producto")
                print("4) Gestionar mis pedidos")
                print("5) Ver mi menú")
                print("0) Cerrar sesión y volver")

                opcion = input("\nSeleccione una opcion: ")

                if opcion == "1":
                    self.agregar_producto()
                elif opcion == "2":
                    self.editar_producto()
                elif opcion == "3":
                    self.eliminar_producto()
                elif opcion == "4":
                    self.gestionar_pedidos()
                elif opcion == "5":
                    self.mostrar_mi_menu()
                elif opcion == "0":
                    self.vendedor_actual = None
                    print("Sesión cerrada.")
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
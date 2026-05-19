from flask import Flask
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash
from modelo.model import Usuario, Vendedor, Producto, SistemaFoodU
from modelo.persistencia import guardar_datos, cargar_datos

app = Flask(__name__)
app.secret_key = "foodu-udem-2024"


#ESTADO GLOBAL DEL SISTEMA


sistema=SistemaFoodU()
id_usuario, id_producto = cargar_datos(sistema)


#HELPERS

def get_usuario_actual():
    nombre = session.get("usuario")
    if nombre:
        return sistema.buscar_usuario(nombre)
    return None

def get_venvedor_actual():
    nombre=session.get("vendedor")
    if nombre:
        return sistema.buscar_vendedor(nombre)
    return None
#RUTAS PRINCIPALES
@app.route("/")
def index():
    return render_template("index.html")


#USUARIO - LIGIN Y REGISTRO
@app.route("/usuario/login", methods=["GET", "POST"])
def login_usuario():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        contrasena = request.form["contrasena"].strip()
        usuario = sistema.buscar_usuario(nombre)
        if usuario is None or usuario.contrasena != contrasena:
            flash("Nombre o contraseña incorrectos.", "error")
            return redirect(url_for("login_usuario"))
        session["usuario"] = usuario.nombre
        flash(f"¡Bienvenido, {usuario.nombre}!", "success")
        return redirect(url_for("dashboard_usuario"))
    return render_template("login_usuario.html")


@app.route("/usuario/registro", methods=["GET", "POST"])
def registro_usuario():
    global id_usuario
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        correo = request.form["correo"].strip()
        tiempo = request.form["tiempo"].strip()
        contrasena = request.form["contrasena"].strip()

        errores = []
        if len(nombre) <= 2:
            errores.append("El nombre debe tener más de 2 caracteres.")
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo):
            errores.append("Correo inválido (ej: usuario@gmail.com).")
        if not tiempo.isdigit():
            errores.append("El tiempo disponible debe ser un número.")
        if len(contrasena) < 4:
            errores.append("La contraseña debe tener al menos 4 caracteres.")

        if errores:
            for e in errores:
                flash(e, "error")
            return redirect(url_for("registro_usuario"))

        usuario = Usuario(id_usuario, nombre, correo, int(tiempo), contrasena)
        resultado = sistema.registrar_usuario(usuario)
        if "correctamente" in resultado:
            id_usuario += 1
            guardar_datos(sistema, id_usuario, id_producto)
            flash("Cuenta creada exitosamente. Inicia sesión.", "success")
            return redirect(url_for("login_usuario"))
        else:
            flash(resultado, "error")
            return redirect(url_for("registro_usuario"))
    return render_template("registro_usuario.html")


@app.route("/usuario/logout")
def logout_usuario():
    session.pop("usuario", None)
    return redirect(url_for("index"))


#USUARIO - DASHBOARD

@app.route("/usuario/dashboard")
def dashboard_usuario():
    usuario = get_usuario_actual()
    if not usuario:
        return redirect(url_for("login_usuario"))
    recomendados = sistema.recomendar_menu(usuario)
    return render_template("dashboard_usuario.html", usuario=usuario, recomendados=recomendados)


@app.route("/usuario/menu")
def menu_productos():
    usuario = get_usuario_actual()
    if not usuario:
        return redirect(url_for("login_usuario"))
    todos_disponibles = []
    for v in sistema.vendedores:
        for p in v.productos:
            if p.disponible:
                todos_disponibles.append((p, v.nombre))
    return render_template("menu_productos.html", usuario=usuario, productos=todos_disponibles)


@app.route("/usuario/pedido", methods=["GET", "POST"])
def crear_pedido():
    global id_producto
    usuario = get_usuario_actual()
    if not usuario:
        return redirect(url_for("login_usuario"))
    todos_disponibles = []
    for v in sistema.vendedores:
        for p in v.productos:
            if p.disponible:
                todos_disponibles.append(p)
    if request.method == "POST":
        ids_seleccionados = request.form.getlist("productos")
        seleccionados = []
        for id_str in ids_seleccionados:
            id_num = int(id_str)
            for p in todos_disponibles:
                if p.id == id_num:
                    seleccionados.append(p)
        if not seleccionados:
            flash("Debes seleccionar al menos un producto.", "error")
            return redirect(url_for("crear_pedido"))
        pedido = sistema.crear_pedido(usuario, seleccionados)
        turno = sistema.asignar_turno(pedido)
        guardar_datos(sistema, id_usuario, id_producto)
        flash(f"¡Pedido #{pedido.id} creado! Tu turno es el #{turno}. Total: ${pedido.total:.2f}", "success")
        return redirect(url_for("historial_usuario"))
    return render_template("crear_pedido.html", usuario=usuario, productos=todos_disponibles)

@app.route("/usuario/historial")
def historial_usuario():
    usuario = get_usuario_actual()
    if not usuario:
        return redirect(url_for("login_usuario"))
    return render_template("historial_usuario.html", usuario=usuario)


@app.route("/usuario/calificar", methods=["GET", "POST"])
def calificar_vendedor():
    usuario = get_usuario_actual()
    if not usuario:
        return redirect(url_for("login_usuario"))
    if request.method == "POST":
        nombre_vendedor = request.form["vendedor"].strip()
        puntuacion = request.form["puntuacion"].strip()
        vendedor = sistema.buscar_vendedor(nombre_vendedor)
        if vendedor is None:
            flash("Vendedor no encontrado.", "error")
        elif not puntuacion.isdigit() or not (1 <= int(puntuacion) <= 5):
            flash("La puntuación debe ser un número del 1 al 5.", "error")
        else:
            usuario.calificar_vendedor(vendedor, int(puntuacion))
            guardar_datos(sistema, id_usuario, id_producto)
            flash(f"¡Calificación registrada para {vendedor.nombre}!", "success")
        return redirect(url_for("calificar_vendedor"))
    return render_template("calificar_vendedor.html", usuario=usuario, vendedores=sistema.vendedores)



@app.route("/vendedor/login", methods=["GET", "POST"])
def login_vendedor():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        contrasena = request.form["contrasena"].strip()
        vendedor = sistema.buscar_vendedor(nombre)
        if vendedor is None or vendedor.contrasena != contrasena:
            flash("Nombre o contraseña incorrectos.", "error")
            return redirect(url_for("login_vendedor"))
        session["vendedor"] = vendedor.nombre
        flash(f"¡Bienvenido, {vendedor.nombre}!", "success")
        return redirect(url_for("dashboard_vendedor"))
    return render_template("login_vendedor.html")


@app.route("/vendedor/registro", methods=["GET", "POST"])
def registro_vendedor():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        contrasena = request.form["contrasena"].strip()
        errores = []
        if len(nombre) <= 2:
            errores.append("El nombre debe tener más de 2 caracteres.")
        if len(contrasena) < 4:
            errores.append("La contraseña debe tener al menos 4 caracteres.")
        if errores:
            for e in errores:
                flash(e, "error")
            return redirect(url_for("registro_vendedor"))
        vendedor = Vendedor(nombre, contrasena)
        resultado = sistema.registrar_vendedor(vendedor)
        if "correctamente" in resultado:
            guardar_datos(sistema, id_usuario, id_producto)
            flash("Cuenta de vendedor creada. Inicia sesión.", "success")
            return redirect(url_for("login_vendedor"))
        else:
            flash(resultado, "error")
            return redirect(url_for("registro_vendedor"))
    return render_template("registro_vendedor.html")


@app.route("/vendedor/logout")
def logout_vendedor():
    session.pop("vendedor", None)
    return redirect(url_for("index"))


@app.route("/vendedor/dashboard")
def dashboard_vendedor():
    vendedor = get_vendedor_actual()
    if not vendedor:
        return redirect(url_for("login_vendedor"))
    congestion = sistema.calcular_congestion(vendedor)
    return render_template("dashboard_vendedor.html", vendedor=vendedor, congestion=congestion)


@app.route("/vendedor/productos/agregar", methods=["GET", "POST"])
def agregar_producto():
    global id_producto
    vendedor = get_vendedor_actual()
    if not vendedor:
        return redirect(url_for("login_vendedor"))
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        precio = request.form["precio"].strip()
        tiempo = request.form["tiempo"].strip()
        disponible = request.form.get("disponible") == "on"
        try:
            producto = Producto(id_producto, nombre, float(precio), int(tiempo), disponible)
            vendedor.agregar_producto(producto)
            id_producto += 1
            guardar_datos(sistema, id_usuario, id_producto)
            flash(f"Producto '{nombre}' agregado correctamente.", "success")
        except:
            flash("Error al agregar el producto. Verifica los datos.", "error")
        return redirect(url_for("dashboard_vendedor"))
    return render_template("agregar_producto.html", vendedor=vendedor)






@app.route("/vendedor/productos/editar/<int:producto_id>", methods=["GET", "POST"])
def editar_producto(producto_id):
    vendedor = get_vendedor_actual()
    if not vendedor:
        return redirect(url_for("login_vendedor"))
    producto = None
    for p in vendedor.productos:
        if p.id == producto_id:
            producto = p
            break
    if not producto:
        flash("Producto no encontrado.", "error")
        return redirect(url_for("dashboard_vendedor"))
    if request.method == "POST":
        nuevo_nombre = request.form["nombre"].strip()
        nuevo_precio = float(request.form["precio"])
        nuevo_tiempo = int(request.form["tiempo"])
        nueva_disp = request.form.get("disponible") == "on"
        vendedor.editar_producto(producto_id, nuevo_nombre, nuevo_precio, nuevo_tiempo, nueva_disp)
        guardar_datos(sistema, id_usuario, id_producto)
        flash("Producto actualizado.", "success")
        return redirect(url_for("dashboard_vendedor"))
    return render_template("editar_producto.html", vendedor=vendedor, producto=producto)


@app.route("/vendedor/productos/eliminar/<int:producto_id>")
def eliminar_producto(producto_id):
    vendedor = get_vendedor_actual()
    if not vendedor:
        return redirect(url_for("login_vendedor"))
    vendedor.eliminar_producto(producto_id)
    guardar_datos(sistema, id_usuario, id_producto)
    flash("Producto eliminado.", "success")
    return redirect(url_for("dashboard_vendedor"))



@app.route("/vendedor/pedidos", methods=["GET", "POST"])
def gestionar_pedidos():
    vendedor = get_vendedor_actual()
    if not vendedor:
        return redirect(url_for("login_vendedor"))
    if request.method == "POST":
        pedido_id = int(request.form["pedido_id"])
        nuevo_estado = request.form["estado"]
        for pedido in vendedor.pedidos_activos:
            if pedido.id == pedido_id:
                pedido.cambiar_estado(nuevo_estado)
                guardar_datos(sistema, id_usuario, id_producto)
                flash(f"Estado del pedido #{pedido_id} actualizado a '{nuevo_estado}'.", "success")
                break
    congestion = sistema.calcular_congestion(vendedor)
    return render_template("gestionar_pedidos.html", vendedor=vendedor, congestion=congestion)


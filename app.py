from flask import Flask
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash
from modelo.model import Usuario, Vendedor, Producto, SistemaFoodU
from modelo.persistencia import guardar_datos, cargar_datos

app = Flask(__name__)
app.secret_key = "foodu-udem-2024"


#ESTADO GLOBAL DEL SISTEMA


sistema=SistemaFoodU()
id_usuario, id_producto = cargar_datos()


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

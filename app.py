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




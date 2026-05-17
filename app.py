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

@app.route("/")
def index():
    return render_template("index.html")



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





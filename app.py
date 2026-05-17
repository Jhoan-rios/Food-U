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





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




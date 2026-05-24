from datetime import datetime

from flask import Flask
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash
from modelo.model import Usuario, Vendedor, Producto, SistemaFoodU
from modelo.persistencia import guardar_datos, cargar_datos
from modelo.horario1 import Horario, Clase
import json as _json_persist
import os
import json
import requests
import bcrypt

app = Flask(__name__)
app.secret_key = "foodu-udem-2024"


#ESTADO GLOBAL DEL SISTEMA


sistema=SistemaFoodU()
id_usuario, id_producto = cargar_datos(sistema)
HORARIOS_FILE = "horarios.json"
horarios: dict = {}

def cargar_horarios():
    if not os.path.exists(HORARIOS_FILE):
        return {}
    try:
        with open(HORARIOS_FILE, "r", encoding="utf-8") as f:
            data = _json_persist.load(f)
        return {nombre: Horario.from_dict(d) for nombre, d in data.items()}
    except Exception:
        return {}

def guardar_horarios(horarios_dict):
    data = {nombre: h.to_dict() for nombre, h in horarios_dict.items()}
    with open(HORARIOS_FILE, "w", encoding="utf-8") as f:
        _json_persist.dump(data, f, ensure_ascii=False, indent=2)

def get_horario_usuario(nombre):
    if nombre not in horarios:
        horarios[nombre] = Horario(nombre)
    return horarios[nombre]

horarios = cargar_horarios()

#HELPERS

def get_usuario_actual():
    nombre = session.get("usuario")
    if nombre:
        return sistema.buscar_usuario(nombre)
    return None

def get_vendedor_actual():
    nombre=session.get("vendedor")
    if nombre:
        return sistema.buscar_vendedor(nombre)
    return None

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
        if usuario is None or not bcrypt.checkpw(contrasena.encode("utf-8"), usuario.contrasena.encode("utf-8")):
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

        contrasena_hash = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        usuario = Usuario(id_usuario, nombre, correo, int(tiempo), contrasena_hash)
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
        if vendedor is None or not bcrypt.checkpw(contrasena.encode("utf-8"), vendedor.contrasena.encode("utf-8")):
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
        contrasena_hash = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        vendedor = Vendedor(nombre, contrasena_hash)
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

# ─────────────────────────────────────────
# PANTALLA PUBLICA DE TURNOS
# ─────────────────────────────────────────
@app.route("/turnos")
def pantalla_turnos():
    return render_template("turnos.html", pedidos=sistema.pedidos, vendedores=sistema.vendedores)




# ─────────────────────────────────────────
# CHATBOT IA
# ─────────────────────────────────────────
@app.route("/chatbot")
def chatbot():
    usuario = get_usuario_actual()
    if not usuario:
        return redirect(url_for("login_usuario"))

    menu = []
    for v in sistema.vendedores:
        for p in v.productos:
            if p.disponible:
                menu.append({
                    "nombre": p.nombre,
                    "precio": p.precio,
                    "tiempo": p.tiempo_preparacion,
                    "vendedor": v.nombre
                })

    menu_json = json.dumps(menu, ensure_ascii=False)
    return render_template("chatbot.html", usuario=usuario, menu_json=menu_json)


@app.route("/chatbot/responder", methods=["POST"])
def chatbot_responder():
    data = request.get_json()
    mensaje_usuario = data.get("mensaje", "")
    menu = data.get("menu", [])

    if menu:
        menu_texto = "Menú disponible ahora mismo:\n"
        for item in menu:
            menu_texto += f"- {item['nombre']} | ${item['precio']} | {item['tiempo']} min | Vendedor: {item['vendedor']}\n"
    else:
        menu_texto = "No hay productos disponibles en este momento."

    sistema_prompt = f"""Eres el asistente virtual de FoodU, una app de pedidos de comida universitaria en Colombia.
Tu trabajo es ayudar a los estudiantes a decidir qué pedir según su tiempo disponible, presupuesto y gustos.
Sé amigable, breve y usa emojis ocasionalmente.
Responde siempre en español.

{menu_texto}

Cuando recomiendes productos, menciona el nombre, precio y tiempo de preparación.
Si el estudiante no tiene mucho tiempo, recomienda lo más rápido.
Si quiere algo económico, recomienda lo más barato."""

    try:
        respuesta = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type": "application/json"},
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 500,
                "system": sistema_prompt,
                "messages": [
                    {"role": "user", "content": mensaje_usuario}
                ]
            }
        )
        data_respuesta = respuesta.json()
        texto = data_respuesta["content"][0]["text"]
        return json.dumps({"respuesta": texto}, ensure_ascii=False), 200, {"Content-Type": "application/json"}

    except Exception as e:
        return json.dumps({"respuesta": "Lo siento, no puedo responder ahora. Intenta más tarde."}, ensure_ascii=False), 200, {"Content-Type": "application/json"}

def get_horario_usuario(nombre: str) -> Horario:
    """Obtiene o crea el horario de un usuario."""
    if nombre not in horarios:
        horarios[nombre] = Horario(nombre)
    return horarios[nombre]


@app.route("/usuario/horario")
def ver_horario():
    usuario = get_usuario_actual()
    if not usuario:
        return redirect(url_for("login_usuario"))

    horario = get_horario_usuario(usuario.nombre)
    resumen = horario.resumen_semanal()

    # Sugerencia en tiempo real
    ahora = datetime.now()
    dia_actual = ["lunes", "martes", "miércoles", "jueves", "viernes",
                  "sábado", "domingo"][ahora.weekday()]
    hora_actual = ahora.strftime("%H:%M")

    sugerencia = None
    if dia_actual in ["lunes", "martes", "miércoles", "jueves", "viernes"]:
        sugerencia = horario.sugerencia_pedido_ahora(hora_actual, dia_actual)

    return render_template(
        "horario.html",
        usuario=usuario,
        horario=horario,
        resumen=resumen,
        sugerencia=sugerencia,
        dias=["lunes", "martes", "miércoles", "jueves", "viernes"],
    )


# ─────────────────────────────────────────
# AGREGAR CLASE AL HORARIO
# ─────────────────────────────────────────

@app.route("/usuario/horario/agregar", methods=["GET", "POST"])
def agregar_clase():
    usuario = get_usuario_actual()
    if not usuario:
        return redirect(url_for("login_usuario"))

    horario = get_horario_usuario(usuario.nombre)

    if request.method == "POST":
        nombre   = request.form["nombre"].strip()
        dia      = request.form["dia"].strip().lower()
        h_inicio = request.form["hora_inicio"].strip()
        h_fin    = request.form["hora_fin"].strip()
        salon    = request.form.get("salon", "").strip()

        try:
            clase = Clase(nombre, dia, h_inicio, h_fin, salon)
            resultado = horario.agregar_clase(clase)
            if "agregada" in resultado:
                flash(resultado, "success")
                # Persistir (integrar con guardar_datos si se desea)
                guardar_horarios(horarios)
            else:
                flash(resultado, "error")
        except Exception as e:
            flash(f"Error: {str(e)}", "error")

        return redirect(url_for("ver_horario"))

    dias = ["lunes", "martes", "miércoles", "jueves", "viernes"]
    return render_template("agregar_clase.html", usuario=usuario, dias=dias)


# ─────────────────────────────────────────
# ELIMINAR CLASE DEL HORARIO
# ─────────────────────────────────────────

@app.route("/usuario/horario/eliminar", methods=["POST"])
def eliminar_clase():
    usuario = get_usuario_actual()
    if not usuario:
        return redirect(url_for("login_usuario"))

    horario = get_horario_usuario(usuario.nombre)
    nombre = request.form["nombre"].strip()
    dia    = request.form["dia"].strip()

    resultado = horario.eliminar_clase(nombre, dia)
    flash(resultado, "success" if "eliminada" in resultado else "error")
    guardar_horarios(horarios)
    return redirect(url_for("ver_horario"))


# ─────────────────────────────────────────
# API: SUGERENCIA EN TIEMPO REAL (JSON)
# ─────────────────────────────────────────

@app.route("/api/horario/sugerencia")
def api_sugerencia():
    """Endpoint que el frontend puede consultar cada minuto via JS."""
    import json as _json
    usuario = get_usuario_actual()
    if not usuario:
        return _json.dumps({"error": "no autenticado"}), 401

    horario = get_horario_usuario(usuario.nombre)
    ahora = datetime.now()
    dia_actual = ["lunes", "martes", "miércoles", "jueves", "viernes",
                  "sábado", "domingo"][ahora.weekday()]
    hora_actual = ahora.strftime("%H:%M")

    if dia_actual not in ["lunes", "martes", "miércoles", "jueves", "viernes"]:
        return _json.dumps({"tiene_espacio": False, "mensaje": "Hoy no hay clases 🎉"})

    sug = horario.sugerencia_pedido_ahora(hora_actual, dia_actual)

    respuesta = {
        "tiene_espacio": sug["tiene_espacio"],
        "mensaje": sug["mensaje"],
        "urgente": sug["urgente"],
        "minutos_faltan": sug["minutos_faltan"],
    }
    if sug["espacio"]:
        esp = sug["espacio"]
        respuesta["espacio"] = {
            "inicio": esp.inicio.strftime("%H:%M"),
            "fin": esp.fin.strftime("%H:%M"),
            "duracion": esp.duracion,
            "modo": esp.modo,
            "punto_venta": esp.punto_venta_sugerido,
        }

    return _json.dumps(respuesta, ensure_ascii=False), 200, {"Content-Type": "application/json"}


# ─────────────────────────────────────────
# CARGA / GUARDADO DE HORARIOS (persistencia)
# ─────────────────────────────────────────

import json as _json_persist
import os

HORARIOS_FILE = "horarios.json"


def cargar_horarios() -> dict[str, Horario]:
    """Carga los horarios desde horarios.json al iniciar la app."""
    if not os.path.exists(HORARIOS_FILE):
        return {}
    try:
        with open(HORARIOS_FILE, "r", encoding="utf-8") as f:
            data = _json_persist.load(f)
        return {nombre: Horario.from_dict(d) for nombre, d in data.items()}
    except Exception:
        return {}


def guardar_horarios(horarios_dict: dict[str, Horario]):
    """Guarda todos los horarios en horarios.json."""
    data = {nombre: h.to_dict() for nombre, h in horarios_dict.items()}
    with open(HORARIOS_FILE, "w", encoding="utf-8") as f:
        _json_persist.dump(data, f, ensure_ascii=False, indent=2)
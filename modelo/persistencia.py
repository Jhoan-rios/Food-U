import json
import os

from modelo.model import Pedido

RUTA_ARCHIVO = "datos.json"

def guardar_datos(sistema, id_usuario, id_producto):
    datos = {
        "id_usuario": id_usuario,
        "id_producto": id_producto,
        "usuarios": [],
        "vendedores": [],
        "pedidos": []
    }

    for u in sistema.usuarios:
        datos["usuarios"].append({
            "id": u.id,
            "nombre": u.nombre,
            "correo": u.correo,
            "tiempo_disponible": 0
        })

    for v in sistema.vendedores:
        vendedor_dict = {
            'nombre': v.nombre,
            'calificacion': v.calificacion,
            'productos': []
        }

        for p in v.productos:
            vendedor_dict["productos"].append({
                "id": p.id,
                "nombre": p.nombre,
                "precio": p.precio,
                "tiempo_preparacion": p.tiempo_preparacion,
                "disponible": p.disponible
            })
        datos["vendedores"].append(vendedor_dict)

    for pedido in sistema.pedidos:
        datos["pedidos"].append({
            'id': pedido.id,
            "usuario_nombre": pedido.usuario.nombre,
            "productos_ids": [p.id for p in pedido.productos],
            "estado": pedido.estado,
            "tiempo_estimado": pedido.tiempo_estimado,
            "total": pedido.total
        })

    with open(RUTA_ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def cargar_datos(sistema):
    from modelo.model import Usuario, Vendedor, Producto

    if not os.path.exists(RUTA_ARCHIVO):
        return 1,1

    if os.path.getsize(RUTA_ARCHIVO) == 0:
        return 1,1

    with open(RUTA_ARCHIVO, "r", encoding="utf-8") as f:
        datos = json.load(f)

    for u_dict in datos["usuarios"]:
        usuario = Usuario(u_dict["id"], u_dict["nombre"], u_dict["correo"], u_dict["tiempo_disponible"])
        sistema.usuarios.append(usuario)

    for v_dict in datos["vendedores"]:
        vendedor = Vendedor(v_dict["nombre"])
        vendedor.calificacion = v_dict["calificacion"]
        for p_dict in v_dict["productos"]:
            producto =Producto(p_dict["id"],p_dict["nombre"],p_dict["precio"],p_dict["tiempo_preparacion"], p_dict["disponible"])
            vendedor.productos.append(producto)
        sistema.vendedores.append(vendedor)

    mapa_productos = {}
    for p_dict in datos.get("pedidos", []):
        usuario = sistema.buscar_usuario(p_dict["usuario_nombre"])
        if usuario is None:
            continue

        pedido = Pedido(p_dict["id"], usuario)
        pedido.estado = p_dict["estado"]
        pedido.tiempo_estimado = p_dict["tiempo_estimado"]
        pedido.total = p_dict["total"]

        for pid in p_dict["productos_ids"]:
            if pid in mapa_productos:
                pedido.productos.append(mapa_productos[pid])

        sistema.pedidos.append(pedido)
        usuario.historial_pedidos.append(pedido)
    return datos["id_usuario"], datos["id_producto"]
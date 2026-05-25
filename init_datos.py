import json
import bcrypt

with open("datos.ejemplo.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

for u in datos["usuarios"]:
    u["contrasena"] = bcrypt.hashpw(
        u["contrasena"].encode(), bcrypt.gensalt()
    ).decode()

for v in datos["vendedores"]:
    v["contrasena"] = bcrypt.hashpw(
        v["contrasena"].encode(), bcrypt.gensalt()
    ).decode()

with open("datos.json", "w", encoding="utf-8") as f:
    json.dump(datos, f, indent=4, ensure_ascii=False)

print("✅ datos.json generado correctamente con contraseñas hasheadas.")
print("   Contraseña de todos los usuarios y vendedores: foodu2024")

"""
FIX: Stale data

Problema:  el caché queda con el valor viejo después de actualizar la DB.
Qué uso:   el mismo dict, cambiando solo la función de escritura.
Solución:  escribir la DB y después BORRAR la clave del caché. La próxima
           lectura no la encuentra y trae el valor nuevo de la DB.
Por qué borrar y no actualizar el caché: si dos escrituras llegan a la vez,
           pueden actualizar el caché en otro orden que la DB y dejar el
           valor equivocado. Borrar siempre deja el caché correcto.

Ejecutar: python errors/01_stale_data_fix.py
"""
DB = {"product:1": 100}  # la "base de datos": el producto cuesta 100
cache = {}               # el caché


def get(key):
    # cache-aside: si no está en caché, se lee de la DB y se guarda
    if key not in cache:
        cache[key] = DB[key]
    return cache[key]


def update(key, value):
    DB[key] = value       # 1. se cambia la DB
    cache.pop(key, None)  # 2. se BORRA la clave del caché. pop(key, None) = "borrar si existe"


get("product:1")         # guarda 100 en el caché
update("product:1", 80)  # la DB pasa a 80 y la clave se borra del caché
print("DB:   ", DB["product:1"])     # 80
print("caché:", get("product:1"))    # no está en caché → lee la DB → 80

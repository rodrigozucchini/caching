"""
ERROR: Stale data (datos viejos)

Problema:  se actualiza la DB pero no el caché.
Qué vas a ver: la DB tiene el precio nuevo y el caché sigue dando el viejo.

Ejecutar: python errors/01_stale_data_error.py
"""
DB = {"product:1": 100}  # la "base de datos": el producto cuesta 100
cache = {}               # el caché


def get(key):
    # cache-aside: si no está en caché, se lee de la DB y se guarda
    if key not in cache:
        cache[key] = DB[key]
    return cache[key]


def update(key, value):
    DB[key] = value  # se cambia la DB... pero el caché sigue con el valor viejo


get("product:1")         # guarda 100 en el caché
update("product:1", 80)  # la DB pasa a 80, el caché sigue en 100
print("DB:   ", DB["product:1"])     # 80
print("caché:", get("product:1"))    # 100: está en caché, así que ni mira la DB

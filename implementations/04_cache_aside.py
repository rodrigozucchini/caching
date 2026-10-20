"""
Cache-aside (la estrategia más usada)

Problema:  la DB es lenta y se leen los mismos datos una y otra vez.
Qué uso:   un dict como caché, delante de la DB.
Solución:  leer:     buscar en caché -> si no está, leer la DB y guardarlo.
           escribir: escribir la DB y BORRAR la clave del caché.
Por qué:   simple, solo cachea lo que realmente se lee, y si el caché se
           cae la app sigue funcionando contra la DB.

Ejecutar: python implementations/04_cache_aside.py
"""
import time

DB = {"user:1": "Ana"}  # la "base de datos"
cache = {}              # el caché: un dict al costado de la DB
db_reads = 0            # cuántas veces se consultó la DB (para ver el efecto)


def db_get(key):
    global db_reads  # global: para poder modificar la variable de afuera
    db_reads += 1
    time.sleep(0.2)  # la DB es lenta
    return DB[key]


def get(key):
    # 1. ¿Está en caché? → se devuelve directo (rápido)
    # 2. ¿No está? → se lee de la DB y se guarda en caché para la próxima
    if key not in cache:
        cache[key] = db_get(key)
    return cache[key]


def update(key, value):
    DB[key] = value       # 1. se escribe en la DB (la fuente de verdad)
    cache.pop(key, None)  # 2. se BORRA del caché. pop(key, None) = "borrar si existe"
                          #    (en Python, del cache[key] da error si la clave no está).
                          #    La próxima lectura no la encuentra y trae el valor nuevo.


# 10 lecturas: la 1ra va a la DB, las otras 9 salen del caché
for _ in range(10):
    get("user:1")
print(f"10 lecturas -> {db_reads} consulta a la DB")

# al actualizar se borra del caché, así que la siguiente lectura va a la DB (2da consulta)
update("user:1", "Ana María")
print("después de actualizar:", get("user:1"), f"({db_reads} consultas)")

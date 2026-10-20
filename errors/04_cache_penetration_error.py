"""
ERROR: Cache penetration

Problema:  se piden claves que no existen en la DB. Como el resultado es
           None, no se guarda en caché y cada request vuelve a la DB.
Qué vas a ver: 100 requests a un id inexistente -> 100 consultas a la DB.

Ejecutar: python errors/04_cache_penetration_error.py
"""
DB = {"user:1": "Ana"}  # el usuario 999 NO existe
cache = {}
db_reads = 0


def db_get(key):
    global db_reads
    db_reads += 1
    return DB.get(key)  # .get devuelve None si la clave no existe


def get(key):
    value = cache.get(key)  # None si no está en caché
    if value is None:
        value = db_get(key)  # para user:999 la DB también devuelve None...
        if value is not None:
            cache[key] = value  # ...y como es None, NO se guarda nada
    return value


# Cada request: caché vacío → DB → None → no se guarda → el siguiente repite todo
for _ in range(100):
    get("user:999")
print(f"100 requests -> {db_reads} consultas a la DB")

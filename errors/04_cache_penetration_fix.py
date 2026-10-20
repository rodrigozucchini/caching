"""
FIX: Cache penetration

Problema:  las claves inexistentes nunca se cachean y siempre van a la DB.
Qué uso:   un valor centinela NOT_FOUND.
Solución:  cachear también el "no existe" (negative caching). En un caché
           real, con un TTL corto por si el dato se crea después.
Por qué:   la DB se consulta una vez por clave inexistente. Se usa un
           centinela y no None para distinguir "no existe" de "no está en caché".
           (Si piden ids distintos cada vez, se agrega un bloom filter).

Ejecutar: python errors/04_cache_penetration_fix.py
"""
DB = {"user:1": "Ana"}  # el usuario 999 NO existe
cache = {}
db_reads = 0

# Valor especial para guardar "ya pregunté y no existe".
# object() crea un objeto único: no se puede confundir con ningún dato real ni con None.
# En general sirve cualquier valor reservado que nunca pueda ser un dato real
# (p. ej. el string "__NOT_FOUND__", que es lo que se haría en Redis).
NOT_FOUND = object()


def db_get(key):
    global db_reads
    db_reads += 1
    return DB.get(key)  # .get devuelve None si la clave no existe


def get(key):
    # "key not in cache" pregunta si la CLAVE existe en el dict, sin importar el valor.
    # Así se distingue "nunca lo busqué" (no está la clave) de "no existe" (está con NOT_FOUND).
    if key not in cache:
        value = db_get(key)
        # Se guarda SIEMPRE: el dato si existe, o NOT_FOUND si no existe
        cache[key] = NOT_FOUND if value is None else value

    value = cache[key]
    # Hacia afuera se devuelve None para "no existe", como antes
    return None if value is NOT_FOUND else value


# 1er request: DB → None → guarda NOT_FOUND. Los otros 99: lo encuentran en caché.
for _ in range(100):
    get("user:999")
print(f"100 requests -> {db_reads} consulta a la DB")

"""
ERROR: Cache penetration

Problema:  se piden claves que no existen en la DB. Como el resultado es
           "nada", no se guarda en caché y cada request vuelve a la DB.
Solución:  cachear también el "no existe" con un valor especial NOT_FOUND
           (negative caching). En un caché real, con TTL corto por si el
           dato se crea después.
Por qué:   la DB se consulta una sola vez por clave inexistente.
           (Si piden ids distintos cada vez, se agrega un bloom filter).

Ejecutar: python errors/04_cache_penetration.py
"""
DB = {"user:1": "Ana"}  # el usuario 999 NO existe
cache = {}
db_reads = 0


def db_get(key):
    global db_reads
    db_reads += 1
    return DB.get(key)  # .get devuelve None si la clave no existe


# ===================== CON ERROR =====================

def get_bad(key):
    value = cache.get(key)  # None si no está en caché
    if value is None:
        value = db_get(key)  # para user:999 la DB también devuelve None...
        if value is not None:
            cache[key] = value  # ...y como es None, NO se guarda nada
    return value


# ===================== SOLUCIÓN ======================

# Valor especial para guardar "ya pregunté y no existe".
# object() crea un objeto único: no se puede confundir con ningún dato real ni con None.
# En general sirve cualquier valor reservado que nunca pueda ser un dato real
# (p. ej. el string "__NOT_FOUND__", que es lo que se haría en Redis).
NOT_FOUND = object()


def get_fixed(key):
    # "key not in cache" pregunta si la CLAVE existe en el dict, sin importar el valor.
    # Así se distingue "nunca lo busqué" (no está la clave) de "no existe" (está con NOT_FOUND).
    if key not in cache:
        value = db_get(key)
        # Se guarda SIEMPRE: el dato si existe, o NOT_FOUND si no existe
        cache[key] = NOT_FOUND if value is None else value

    value = cache[key]
    # Hacia afuera se devuelve None para "no existe", como antes
    return None if value is NOT_FOUND else value


# ======================= DEMO ========================

def simulate(get_function):
    """100 requests al mismo id inexistente. Devuelve cuántas veces se consultó la DB."""
    global db_reads
    cache.clear()
    db_reads = 0
    for _ in range(100):
        get_function("user:999")
    return db_reads


# con error: cada request → caché vacío → DB → None → no se guarda → el siguiente repite todo
print(f"con error: 100 requests -> {simulate(get_bad)} consultas a la DB  ✗")
# solución: 1er request → DB → guarda NOT_FOUND. Los otros 99 lo encuentran en caché.
print(f"solución:  100 requests -> {simulate(get_fixed)} consulta a la DB  ✓")

"""
ERROR: Caché sin límite

Problema:  un diccionario usado como caché nunca borra nada. Si las claves
           casi no se repiten (búsquedas, ids de request), crece hasta
           llenar la memoria.
Solución:  un tamaño máximo; cuando el caché está lleno, antes de agregar
           algo nuevo se borra la entrada que hace más tiempo nadie usa
           (LRU, ver implementations/07_lru.py).
Por qué:   la memoria queda acotada pase lo que pase, y se conservan las
           entradas que se están usando. En Redis el equivalente es
           configurar maxmemory + una política de borrado (allkeys-lru).

Ejecutar: python errors/06_unbounded_cache.py
"""

# ===================== CON ERROR =====================

cache_bad = {}  # un dict no tiene tamaño máximo


def search_bad(query):
    if query not in cache_bad:
        cache_bad[query] = f"resultados de {query}"  # se agrega y nunca se borra
    return cache_bad[query]


# ===================== SOLUCIÓN ======================

MAX_SIZE = 1000  # el caché nunca va a tener más de 1000 entradas

cache_fixed = {}
order = []  # claves ordenadas por uso: order[0] = la que hace más tiempo nadie usa


def search_fixed(query):
    if query in cache_fixed:
        order.remove(query)  # se usó → pasa al final de la lista
        order.append(query)
        return cache_fixed[query]

    result = f"resultados de {query}"
    if len(cache_fixed) >= MAX_SIZE:
        oldest = order.pop(0)    # caché lleno: se saca la menos usada...
        del cache_fixed[oldest]  # ...y se borra para hacer lugar
    cache_fixed[query] = result
    order.append(query)
    return result

# Nota: en Python, @functools.lru_cache(maxsize=1000) hace todo esto en una línea.


# ======================= DEMO ========================

# 100.000 búsquedas distintas
for i in range(100_000):
    search_bad(f"query {i}")
    search_fixed(f"query {i}")

print(f"con error: {len(cache_bad)} entradas en memoria (y sigue creciendo)  ✗")
print(f"solución:  {len(cache_fixed)} entradas en memoria (nunca más de {MAX_SIZE})  ✓")

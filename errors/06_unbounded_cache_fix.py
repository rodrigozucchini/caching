"""
FIX: Caché sin límite

Problema:  el caché crece sin parar hasta quedarse sin memoria.
Qué uso:   el mismo diccionario + un tamaño máximo + una lista con el orden de uso.
Solución:  cuando el caché llega al máximo, antes de agregar algo nuevo se
           borra la entrada que hace más tiempo nadie usa (LRU, ver
           implementations/07_lru.py).
Por qué:   la memoria queda acotada pase lo que pase, y se conservan las
           entradas que se están usando. En Redis el equivalente es
           configurar maxmemory + una política de borrado (allkeys-lru).

Ejecutar: python errors/06_unbounded_cache_fix.py
"""
MAX_SIZE = 1000  # el caché nunca va a tener más de 1000 entradas

cache = {}
order = []  # claves ordenadas por uso: order[0] = la que hace más tiempo nadie usa


def search(query):
    if query in cache:
        order.remove(query)  # se usó → pasa al final de la lista
        order.append(query)
        return cache[query]

    result = f"resultados de {query}"
    if len(cache) >= MAX_SIZE:
        oldest = order.pop(0)  # caché lleno: se saca la menos usada...
        del cache[oldest]      # ...y se borra para hacer lugar
    cache[query] = result
    order.append(query)
    return result

# Nota: en Python, @functools.lru_cache(maxsize=1000) hace todo esto en una línea.


for i in range(100_000):
    search(f"query {i}")
print(f"entradas en caché: {len(cache)} (nunca más de {MAX_SIZE})")

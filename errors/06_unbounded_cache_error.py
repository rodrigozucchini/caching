"""
ERROR: Caché sin límite

Problema:  un dict usado como caché nunca borra nada. Si las claves casi no
           se repiten (búsquedas, ids de request), crece hasta llenar la memoria.
Qué vas a ver: 100.000 búsquedas distintas -> 100.000 entradas en memoria.

Ejecutar: python errors/06_unbounded_cache_error.py
"""
cache = {}  # un dict no tiene tamaño máximo


def search(query):
    if query not in cache:
        cache[query] = f"resultados de {query}"  # se agrega y nunca se borra
    return cache[query]


# 100.000 búsquedas distintas → 100.000 entradas que quedan en memoria para siempre,
# aunque la mayoría nunca se vuelva a pedir
for i in range(100_000):
    search(f"query {i}")
print(f"entradas en caché: {len(cache)} (y sigue creciendo)")

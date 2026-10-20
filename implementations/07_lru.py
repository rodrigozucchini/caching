"""
LRU (Least Recently Used)

Problema:  la memoria es limitada; cuando el caché se llena, ¿qué se borra?
Qué uso:   un diccionario para los valores + una lista con las claves
           ordenadas por último uso.
Solución:  al usar una clave se mueve al final de la lista; al llenarse se
           borra la del principio, que es la que hace más tiempo nadie usa.
Por qué:   lo usado hace poco suele volver a usarse; lo que nadie pide hace
           rato, probablemente no. Es la política más usada.

Ejecutar: python implementations/07_lru.py
"""
CAPACITY = 3  # máximo de claves que entran en el caché

cache = {}  # clave -> valor
order = []  # claves ordenadas por uso: order[0] = la menos reciente, order[-1] = la más reciente

# Nota: con una lista, mover o borrar una clave tiene que recorrerla (lento con
# muchas claves). Las implementaciones reales usan una lista doblemente enlazada
# + diccionario, que hace todo sin recorrer nada. En Python eso ya existe:
# collections.OrderedDict. Acá se usa una lista común para que se vea la idea.


def touch(key):
    """Marca la clave como la más reciente: la saca de donde esté y la pone al final."""
    if key in order:
        order.remove(key)
    order.append(key)


def get(key):
    if key not in cache:
        return None
    touch(key)  # se acaba de usar → pasa al final
    return cache[key]


def put(key, value):
    cache[key] = value
    touch(key)  # recién guardada → también es la más reciente
    if len(cache) > CAPACITY:
        oldest = order.pop(0)  # saca la primera de la lista: la menos usada
        del cache[oldest]
        print(f"  caché lleno, se borra '{oldest}'")


put("A", 1)  # order = [A]
put("B", 2)  # order = [A, B]
put("C", 3)  # order = [A, B, C]
get("A")     # order = [B, C, A]   A se usó → pasa al final; ahora la menos usada es B
put("D", 4)  # order = [B, C, A, D] → se pasa de 3 → se borra B → [C, A, D]
print("orden de uso:", order)

"""
FIX: Objetos mutables en caché

Problema:  quien recibe el valor cacheado lo modifica y corrompe el caché.
Qué uso:   el mismo caché, pero devolviendo una COPIA del valor.
Solución:  el caché guarda el original y a cada lector le entrega una copia.
           Cada uno puede hacer lo que quiera con la suya.
Por qué:   el original nunca sale del caché, así que nadie puede modificarlo.
           Alternativa: guardar valores inmutables (que no se pueden
           modificar); en Python, un tuple en vez de una lista. Es más barato
           porque no copia en cada lectura, pero no todos los datos se pueden
           representar así.

Ejecutar: python errors/07_mutable_cached_object_fix.py
"""
cache = {}


def get_permissions(role):
    if role not in cache:
        cache[role] = ["read"]
    # list(...) crea una lista NUEVA con los mismos elementos: una copia.
    # Si la lista tuviera objetos adentro (listas, dicts), también habría que
    # copiarlos: eso se llama copia profunda (en Python: copy.deepcopy).
    return list(cache[role])


perms = get_permissions("viewer")  # perms es una copia
perms.append("write")              # se modifica la copia, no el caché

print("permisos del request:", perms)                    # ['read', 'write']
print("permisos de viewer:  ", get_permissions("viewer"))  # ['read'] intacto

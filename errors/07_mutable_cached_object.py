"""
ERROR: Objetos mutables en caché

Problema:  un caché en memoria devuelve el MISMO objeto a todos. Si alguien
           lo modifica (por ejemplo, agrega algo a una lista), modifica el
           que está guardado en el caché, y todos lo ven modificado.
Solución:  el caché guarda el original y a cada lector le entrega una COPIA.
Por qué:   el original nunca sale del caché, así que nadie puede modificarlo.
           Alternativa: guardar valores inmutables (que no se pueden
           modificar); en Python, un tuple en vez de una lista. Es más barato
           porque no copia en cada lectura.

Ejecutar: python errors/07_mutable_cached_object.py
"""
cache = {}


# ===================== CON ERROR =====================

def get_permissions_bad(role):
    if role not in cache:
        cache[role] = ["read"]  # se guarda una lista (se puede modificar)
    return cache[role]          # se devuelve la lista del caché, NO una copia


# ===================== SOLUCIÓN ======================

def get_permissions_fixed(role):
    if role not in cache:
        cache[role] = ["read"]
    # list(...) crea una lista NUEVA con los mismos elementos: una copia.
    # Si la lista tuviera objetos adentro (listas, dicts), también habría que
    # copiarlos: eso se llama copia profunda (en Python: copy.deepcopy).
    return list(cache[role])


# ======================= DEMO ========================

print("--- con error ---")
perms = get_permissions_bad("viewer")  # perms apunta a la MISMA lista del caché
perms.append("write")                  # se quería agregar "write" solo para este request...
print("permisos de viewer:", get_permissions_bad("viewer"))  # ['read', 'write']  ✗

print("--- solución ---")
cache.clear()
perms = get_permissions_fixed("viewer")  # perms es una copia
perms.append("write")                    # se modifica la copia, no el caché
print("permisos del request:", perms)                          # ['read', 'write']
print("permisos de viewer:  ", get_permissions_fixed("viewer"))  # ['read']  ✓

"""
ERROR: Objetos mutables en caché

Problema:  un caché en memoria devuelve el MISMO objeto a todos. Si alguien
           lo modifica (por ejemplo, agrega algo a una lista), modifica el
           que está guardado en el caché, y todos los que lo lean después
           ven el cambio.
Qué vas a ver: un request le agrega "write" a sus permisos y desde ahí
               todos los viewers pueden escribir.

Ejecutar: python errors/07_mutable_cached_object_error.py
"""
cache = {}


def get_permissions(role):
    if role not in cache:
        cache[role] = ["read"]  # se guarda una lista (se puede modificar)
    return cache[role]          # se devuelve la lista del caché, NO una copia


# perms apunta a la misma lista que está guardada en el caché
perms = get_permissions("viewer")
perms.append("write")  # se quería agregar "write" solo para este request...

# ...pero se modificó la lista del caché, así que todos los que la pidan la ven así
print("permisos de viewer:", get_permissions("viewer"))  # ['read', 'write']

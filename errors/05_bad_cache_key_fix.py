"""
FIX: Clave de caché mal construida

Problema:  usuarios distintos comparten la misma clave y ven datos ajenos.
Qué uso:   un f-string con todos los parámetros.
Solución:  la clave incluye todo lo que cambia el resultado:
           f"dashboard:{user_id}". Si dependiera de idioma, moneda, etc.,
           también van en la clave.
Por qué:   cada combinación de parámetros tiene su propia entrada, así que
           es imposible devolverle a alguien un resultado que no es suyo.
           El ":" separa los valores y evita colisiones ("1"+"23" vs "12"+"3").

Ejecutar: python errors/05_bad_cache_key_fix.py
"""
DB = {1: "Ana: $5000", 2: "Beto: $20"}  # datos privados de cada usuario
cache = {}


def dashboard(user_id):
    # La clave incluye el user_id: "dashboard:1", "dashboard:2", ...
    # Cada usuario tiene su propia entrada en el caché.
    # (f"..." es Python; es lo mismo que concatenar "dashboard:" + user_id)
    key = f"dashboard:{user_id}"
    if key not in cache:
        cache[key] = DB[user_id]
    return cache[key]


print("Ana ve: ", dashboard(1))  # "dashboard:1" → datos de Ana
print("Beto ve:", dashboard(2))  # "dashboard:2" → datos de Beto

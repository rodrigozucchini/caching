"""
ERROR: Clave de caché mal construida

Problema:  el resultado depende del usuario pero la clave no lo incluye.
           El primero que entra deja sus datos en caché y los demás los ven.
Solución:  la clave incluye todo lo que cambia el resultado:
           "dashboard:" + user_id. Si dependiera de idioma, moneda, etc.,
           también van en la clave.
Por qué:   cada combinación de parámetros tiene su propia entrada, así que
           es imposible devolverle a alguien un resultado que no es suyo.
           El ":" separa los valores y evita colisiones ("1"+"23" vs "12"+"3").

Ejecutar: python errors/05_bad_cache_key.py
"""
DB = {1: "Ana: $5000", 2: "Beto: $20"}  # datos privados de cada usuario
cache = {}


# ===================== CON ERROR =====================

def dashboard_bad(user_id):
    # La clave es siempre la misma, sin importar quién pide.
    # El resultado depende de user_id, pero la clave no lo incluye.
    key = "dashboard"
    if key not in cache:
        cache[key] = DB[user_id]
    return cache[key]


# ===================== SOLUCIÓN ======================

def dashboard_fixed(user_id):
    # La clave incluye el user_id: "dashboard:1", "dashboard:2", ...
    # Cada usuario tiene su propia entrada en el caché.
    # (f"..." es Python; es lo mismo que concatenar "dashboard:" + user_id)
    key = f"dashboard:{user_id}"
    if key not in cache:
        cache[key] = DB[user_id]
    return cache[key]


# ======================= DEMO ========================

print("--- con error ---")
print("Ana ve: ", dashboard_bad(1))  # "dashboard" no está → guarda los datos de Ana
print("Beto ve:", dashboard_bad(2))  # "dashboard" ya está → devuelve los datos de Ana  ✗

print("--- solución ---")
cache.clear()
print("Ana ve: ", dashboard_fixed(1))  # "dashboard:1" → datos de Ana
print("Beto ve:", dashboard_fixed(2))  # "dashboard:2" → datos de Beto  ✓

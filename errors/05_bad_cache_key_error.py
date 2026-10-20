"""
ERROR: Clave de caché mal construida

Problema:  el resultado depende del usuario pero la clave no lo incluye.
           El primero que entra deja sus datos en caché y los demás los ven.
Qué vas a ver: Beto ve el saldo de Ana (fuga de datos).

Ejecutar: python errors/05_bad_cache_key_error.py
"""
DB = {1: "Ana: $5000", 2: "Beto: $20"}  # datos privados de cada usuario
cache = {}


def dashboard(user_id):
    # La clave es siempre la misma, sin importar quién pide.
    # El resultado depende de user_id, pero la clave no lo incluye.
    key = "dashboard"
    if key not in cache:
        cache[key] = DB[user_id]
    return cache[key]


print("Ana ve: ", dashboard(1))  # "dashboard" no está → guarda los datos de Ana
print("Beto ve:", dashboard(2))  # "dashboard" ya está → devuelve los datos de Ana

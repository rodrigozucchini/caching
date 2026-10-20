"""
Write-through

Problema:  con cache-aside, lo que se acaba de escribir no está en caché y
           la primera lectura siempre va a la DB.
Qué uso:   un dict como caché, y toda escritura pasa por él.
Solución:  al escribir, guardar en la DB y en el caché en la misma operación.
Por qué:   el caché siempre tiene el último valor; sirve cuando lo que se
           escribe se lee enseguida (carrito, sesión, perfil).
Costo:     cada escritura espera a la DB.

Ejecutar: python implementations/05_write_through.py
"""
import time

DB = {}     # la "base de datos"
cache = {}  # el caché


def write(key, value):
    # Toda escritura actualiza las DOS cosas, una después de la otra:
    time.sleep(0.2)     # escribir en la DB tarda (por eso las escrituras son más lentas)
    DB[key] = value     # 1. la DB
    cache[key] = value  # 2. el caché, con el mismo valor


def read(key):
    # Lo que se escribió con write() siempre está en caché,
    # así que la lectura nunca tiene que ir a la DB.
    return cache[key]


write("cart:7", ["libro"])
print("lectura inmediata desde el caché:", read("cart:7"))

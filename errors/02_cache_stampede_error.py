"""
ERROR: Cache stampede

Problema:  una clave muy pedida no está en caché (venció o recién arranca)
           y muchos requests llegan al mismo tiempo: todos ven que falta y
           todos van a la DB a buscar lo mismo.
Qué vas a ver: 20 requests simultáneos -> 20 consultas a la DB.

Ejecutar: python errors/02_cache_stampede_error.py
"""
import threading
import time

cache = {}
db_reads = 0  # cuántas veces se consultó la DB


def db_get(key):
    global db_reads
    db_reads += 1
    time.sleep(0.5)  # consulta pesada: mientras dura, el caché sigue vacío
    return "top 100"


def get(key):
    # Los 20 threads llegan a este if casi al mismo tiempo. Como el primero
    # todavía no terminó de consultar la DB, el caché sigue vacío y los 20
    # ven "no está" → los 20 van a la DB.
    if key not in cache:
        cache[key] = db_get(key)
    return cache[key]


# Se crean 20 threads = 20 requests que piden "ranking" al mismo tiempo
threads = [threading.Thread(target=get, args=("ranking",)) for _ in range(20)]
for t in threads:
    t.start()  # arrancan todos casi juntos
for t in threads:
    t.join()   # se espera a que terminen todos

print(f"20 requests -> {db_reads} consultas a la DB")

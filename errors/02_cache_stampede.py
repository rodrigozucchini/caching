"""
ERROR: Cache stampede

Problema:  una clave muy pedida no está en caché (venció o recién arranca)
           y muchos requests llegan al mismo tiempo: todos ven que falta y
           todos van a la DB a buscar lo mismo.
Solución:  un lock: solo uno puede ir a la DB; los demás esperan y cuando
           entran vuelven a mirar el caché (ya está cargado).
Por qué:   N consultas se convierten en 1. Con varias instancias de la app
           se hace igual pero con un lock en Redis (SET lock:clave 1 NX EX 5).

Ejecutar: python errors/02_cache_stampede.py
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


# ===================== CON ERROR =====================

def get_bad(key):
    # Los 20 threads llegan a este if casi al mismo tiempo. Como el primero
    # todavía no terminó de consultar la DB, el caché sigue vacío y los 20
    # ven "no está" → los 20 van a la DB.
    if key not in cache:
        cache[key] = db_get(key)
    return cache[key]


# ===================== SOLUCIÓN ======================

lock = threading.Lock()  # un candado: solo un thread a la vez puede estar adentro


def get_fixed(key):
    # Camino rápido: si ya está, se devuelve sin tocar el lock
    if key in cache:
        return cache[key]

    # "with lock": el primer thread que llega entra; los demás se quedan
    # esperando acá hasta que el primero salga.
    # (with es sintaxis de Python: equivale a lock.acquire() al entrar y
    # lock.release() al salir, incluso si hay un error en el medio)
    with lock:
        # Se vuelve a preguntar ADENTRO del lock. Para el primer thread no está
        # → consulta la DB. Para los que esperaban, el primero ya lo guardó
        # → está → no consultan la DB.
        if key not in cache:
            cache[key] = db_get(key)
    return cache[key]


# ======================= DEMO ========================

def simulate(get_function):
    """Lanza 20 threads (= 20 requests) que piden "ranking" al mismo tiempo."""
    global db_reads
    cache.clear()
    db_reads = 0
    threads = [threading.Thread(target=get_function, args=("ranking",)) for _ in range(20)]
    for t in threads:
        t.start()  # arrancan todos casi juntos
    for t in threads:
        t.join()   # se espera a que terminen todos
    return db_reads


print(f"con error: 20 requests -> {simulate(get_bad)} consultas a la DB  ✗")
print(f"solución:  20 requests -> {simulate(get_fixed)} consulta a la DB  ✓")

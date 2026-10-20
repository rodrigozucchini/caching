"""
FIX: Cache stampede

Problema:  muchos requests simultáneos van a la DB por la misma clave.
Qué uso:   threading.Lock.
Solución:  solo uno puede ir a la DB; los demás esperan el lock y cuando
           entran vuelven a mirar el caché (ya está cargado).
Por qué:   N consultas se convierten en 1 sin cambiar nada más.
           Con varias instancias se hace igual pero con un lock en Redis
           (SET lock:clave 1 NX EX 5).

Ejecutar: python errors/02_cache_stampede_fix.py
"""
import threading
import time

cache = {}
lock = threading.Lock()  # un candado: solo un thread a la vez puede estar adentro
db_reads = 0  # cuántas veces se consultó la DB


def db_get(key):
    global db_reads
    db_reads += 1
    time.sleep(0.5)  # consulta pesada: mientras dura, el caché sigue vacío
    return "top 100"


def get(key):
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


# Se crean 20 threads = 20 requests que piden "ranking" al mismo tiempo
threads = [threading.Thread(target=get, args=("ranking",)) for _ in range(20)]
for t in threads:
    t.start()  # arrancan todos casi juntos
for t in threads:
    t.join()   # se espera a que terminen todos

print(f"20 requests -> {db_reads} consulta a la DB")

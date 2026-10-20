"""
Caché en memoria con TTL

Problema:  el dato cambia con el tiempo (cotizaciones, configuración) y
           la memoización (01) lo guarda para siempre.
Qué uso:   un dict que guarda (valor, momento_de_vencimiento).
Solución:  al leer, si ya venció se borra y se trata como si no estuviera.
Por qué:   es lo mínimo para que el caché no sirva datos viejos para siempre;
           sin dependencias. time.monotonic no se rompe si cambia la hora del sistema.

Ejecutar: python implementations/02_in_memory_ttl.py
"""
import time

# El caché es un dict común. Cada valor se guarda junto con el momento en que vence:
#   cache = { "dolar": (1000, 12345.6) }
#                       ↑      ↑
#                     valor  vence_en (en segundos de time.monotonic())
cache = {}


def cache_set(key, value, ttl):
    # time.monotonic() = segundos desde un punto fijo (un reloj que no salta si
    # alguien cambia la hora del sistema; usar la hora normal también funciona,
    # pero puede fallar en ese caso). Sumándole el ttl
    # obtenemos el momento exacto en que esta entrada deja de ser válida.
    cache[key] = (value, time.monotonic() + ttl)


def cache_get(key):
    if key not in cache:
        return None  # nunca se guardó (o ya se borró)

    value, expires_at = cache[key]  # separa la tupla en sus dos partes

    if time.monotonic() > expires_at:
        # ya pasó el momento de vencimiento: se borra para liberar memoria
        # y se responde como si no existiera, así quien llama busca el dato nuevo
        del cache[key]
        return None

    return value  # todavía es válido


cache_set("dolar", 1000, ttl=1)          # válido durante 1 segundo
print("inmediato:", cache_get("dolar"))   # 1000
time.sleep(1.1)                           # esperamos a que venza
print("después de 1s:", cache_get("dolar"))  # None

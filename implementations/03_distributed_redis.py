"""
Caché distribuido (Redis)

Problema:  la app corre en varias instancias; con caché en memoria cada una
           tiene su copia, todas consultan la DB por lo mismo y pueden
           tener valores distintos.
Qué uso:   Redis (acá fakeredis: Redis en memoria, misma API, sin Docker).
Solución:  todas las instancias leen y escriben el mismo Redis, con
           SET key valor EX segundos para el TTL.
Por qué:   un solo caché compartido; lo que carga una instancia le sirve a
           las demás. TTL incluido y sobrevive a reinicios de la app.

Requiere: pip install fakeredis
Ejecutar: python implementations/03_distributed_redis.py
"""
import time

import fakeredis

# FakeServer es el "servidor Redis" (en memoria, dentro de este proceso).
# Las dos apps se conectan al MISMO server, como dos servidores reales
# conectados al mismo Redis.
server = fakeredis.FakeServer()
# Con un Redis real: redis.Redis(host="localhost", decode_responses=True)
# fakeredis es solo para Python, pero los comandos (GET, SET ... EX) son los de
# Redis: son iguales desde cualquier lenguaje que se conecte a Redis.

# Dos clientes = dos instancias de la app.
# decode_responses=True hace que Redis devuelva str en vez de bytes.
app_a = fakeredis.FakeRedis(server=server, decode_responses=True)
app_b = fakeredis.FakeRedis(server=server, decode_responses=True)

DB = {"user:1": "Ana"}  # la "base de datos"


def db_get(key):
    time.sleep(0.2)  # la DB es lenta
    print(f"  -> consulta a la DB por {key}")
    return DB[key]


def get_user(redis_client, key):
    # GET: pide la clave a Redis. Devuelve None si no existe o ya venció.
    value = redis_client.get(key)
    if value is None:
        value = db_get(key)
        # SET con ex=60: guarda la clave y Redis la borra solo a los 60 segundos (TTL)
        redis_client.set(key, value, ex=60)
    return value


# app A no encuentra la clave en Redis → va a la DB → la guarda en Redis
print("app A:", get_user(app_a, "user:1"))
# app B la encuentra en Redis (la dejó app A) → no toca la DB
print("app B:", get_user(app_b, "user:1"))

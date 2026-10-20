"""
ERROR: Cache avalanche

Problema:  muchas claves se cargan juntas (al arrancar, un job) con el mismo
           TTL, así que vencen todas en el mismo segundo y en ese momento
           todo el tráfico cae sobre la DB.
Qué vas a ver: las 1000 claves vencen en el mismo segundo.

Ejecutar: python errors/03_cache_avalanche_error.py
"""
from collections import Counter  # Python: un dict que cuenta. Es lo mismo que un dict
                                 # segundo -> cantidad, sumando 1 en un for.

TTL = 60  # todas las claves duran 60 segundos
now = 0   # momento en que se cargan (todas juntas, en el segundo 0)

# Se cargan 1000 claves y se calcula cuándo vence cada una: 0 + 60 = 60 para todas
expires_at = {f"item:{i}": now + TTL for i in range(1000)}

# Counter cuenta cuántas claves vencen en cada segundo: {60: 1000}
per_second = Counter(int(t) for t in expires_at.values())
# most_common(1) devuelve el segundo con más vencimientos
second, count = per_second.most_common(1)[0]
print(f"{count} claves vencen en el segundo {second} -> {count} consultas a la DB de golpe")

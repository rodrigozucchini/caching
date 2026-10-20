"""
ERROR: Cache avalanche

Problema:  muchas claves se cargan juntas (al arrancar, un job) con el mismo
           TTL, así que vencen todas en el mismo segundo y en ese momento
           todo el tráfico cae sobre la DB.
Solución:  sumar al TTL un valor aleatorio (jitter), por ejemplo ±10 segundos.
Por qué:   los vencimientos se reparten en el tiempo y la DB recibe la carga
           de a poco en vez de toda junta. Es un cambio de una línea.

Ejecutar: python errors/03_cache_avalanche.py
"""
import random
from collections import Counter  # Python: un dict que cuenta. Es lo mismo que un dict
                                 # segundo -> cantidad, sumando 1 en un for.

TTL = 60  # todas las claves duran 60 segundos
now = 0   # momento en que se cargan (todas juntas, en el segundo 0)


# ===================== CON ERROR =====================

def ttl_bad():
    return TTL  # siempre 60 → todas vencen en 0 + 60 = 60


# ===================== SOLUCIÓN ======================

def ttl_fixed():
    # 60 más un número al azar entre -10 y +10: una clave vence a los 53.2s,
    # otra a los 67.8s, otra a los 58.1s...
    # (random.uniform(a, b) = número decimal aleatorio entre a y b)
    return TTL + random.uniform(-10, 10)


# ======================= DEMO ========================

def worst_second(ttl_function):
    """Carga 1000 claves y devuelve el segundo con más vencimientos."""
    expires_at = [now + ttl_function() for _ in range(1000)]
    per_second = Counter(int(t) for t in expires_at)  # segundo -> cuántas vencen
    return per_second.most_common(1)[0]               # (segundo, cantidad) con más vencimientos


second, count = worst_second(ttl_bad)
print(f"con error: {count} claves vencen en el segundo {second} → todas a la DB juntas  ✗")
second, count = worst_second(ttl_fixed)
print(f"solución:  como mucho {count} claves vencen en el mismo segundo  ✓")

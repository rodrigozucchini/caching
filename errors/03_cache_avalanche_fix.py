"""
FIX: Cache avalanche

Problema:  muchas claves con el mismo TTL vencen juntas.
Qué uso:   un número aleatorio sumado al TTL (jitter).
Solución:  sumar al TTL un valor aleatorio (jitter), por ejemplo ±10 segundos.
Por qué:   los vencimientos se reparten en el tiempo y la DB recibe la carga
           de a poco en vez de toda junta. Es un cambio de una línea.

Ejecutar: python errors/03_cache_avalanche_fix.py
"""
import random
from collections import Counter  # Python: un dict que cuenta. Es lo mismo que un dict
                                 # segundo -> cantidad, sumando 1 en un for.

TTL = 60
now = 0

# Igual que antes, pero a cada TTL se le suma un número al azar entre -10 y +10
# (random.uniform(a, b) = número decimal aleatorio entre a y b).
# Así una clave vence a los 53.2s, otra a los 67.8s, otra a los 58.1s...
expires_at = {f"item:{i}": now + TTL + random.uniform(-10, 10) for i in range(1000)}

# Se cuenta cuántas vencen en cada segundo (int() redondea 53.2 → 53)
per_second = Counter(int(t) for t in expires_at.values())
second, count = per_second.most_common(1)[0]
print(f"vencimientos repartidos entre el segundo {min(per_second)} y el {max(per_second)}")
print(f"máximo en un mismo segundo: {count} (antes 1000)")

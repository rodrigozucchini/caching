# Cache penetration

## El problema

Se piden claves que **no existen** en la DB (un id inválido, un bot). Cada
request atraviesa el caché y llega a la DB.

```
 get("user:999") ──► caché: no está ──► DB: None ──► no se guarda nada
 get("user:999") ──► caché: no está ──► DB: None ──► no se guarda nada
 ... x100

 100 requests = 100 consultas  ✗
```

## Por qué pasa

El código solo guarda en caché cuando encuentra algo (`if value is not None`).
Como "no existe" nunca se guarda, el caché nunca puede responder por esa
clave y la DB recibe todo. Un atacante lo aprovecha pidiendo ids inexistentes
para tumbar la DB.

## La solución

Guardar también el "no existe" en el caché, con un valor especial
`NOT_FOUND` (esto se llama *negative caching*).

```
 get("user:999") ──► caché: no está ──► DB: None ──► guarda NOT_FOUND
 get("user:999") ──► caché: NOT_FOUND ──► devuelve None   (sin ir a la DB)
 ... x99

 100 requests = 1 consulta  ✓
```

## Por qué funciona

Ahora el caché tiene una respuesta para esa clave: "ya pregunté, no existe".
Se usa `NOT_FOUND` y no `None` porque `cache.get(key)` ya devuelve `None`
cuando la clave no está; con `None` no se podría distinguir "no existe" de
"nunca lo busqué".

En un caché real se le pone un TTL corto (p. ej. 30s), por si el usuario se
crea después. Si cada request pide un id distinto, esto no alcanza y se usa
un *bloom filter* con todos los ids que existen.

## En el código

```python
if key not in cache:
    value = db_get(key)
    cache[key] = NOT_FOUND if value is None else value   # ← también "no existe"
```

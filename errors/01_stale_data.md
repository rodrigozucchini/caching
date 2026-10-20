# Stale data (datos viejos)

## El problema

Se actualiza el precio en la DB, pero el caché sigue guardando el precio
anterior. Todos los que leen desde el caché ven un dato que ya no es cierto.

```
 1. get("product:1")      caché vacío → lee DB → guarda 100 en caché
 2. update(..., 80)       escribe 80 en la DB... y nada más

    ┌──────────┐        ┌───────────┐
    │ DB:   80 │   ≠    │ caché: 100│
    └──────────┘        └───────────┘

 3. get("product:1")      está en caché → devuelve 100  ✗
```

## Por qué pasa

Hay dos copias del mismo dato (DB y caché) y la función `update` solo cambia
una. El caché no tiene forma de enterarse de que la DB cambió: mientras la
clave exista en caché, `get` la devuelve sin mirar la DB.

## La solución

Cuando se escribe en la DB, **borrar** la clave del caché.

```
 1. get("product:1")      caché vacío → lee DB → guarda 100
 2. update(..., 80)       escribe 80 en la DB
                          borra "product:1" del caché   ◄── el fix

    ┌──────────┐        ┌───────────┐
    │ DB:   80 │        │ caché: -- │
    └──────────┘        └───────────┘

 3. get("product:1")      no está en caché → lee DB → 80  ✓
```

## Por qué funciona

Al borrar la clave, la próxima lectura es un "miss" y se ve obligada a ir a la
DB, que tiene el valor correcto. El caché se vuelve a llenar solo, con el dato
nuevo.

**¿Por qué borrar y no guardar directamente el 80 en el caché?** Si dos
requests actualizan a la vez, pueden escribir la DB en un orden y el caché en
el orden contrario:

```
 request A: DB = 80                 request B: DB = 70
 request B: caché = 70              request A: caché = 80   → DB 70, caché 80 ✗
```

Borrar no tiene ese problema: borrar dos veces da el mismo resultado (caché
vacío) sin importar el orden, y el siguiente lector trae lo que diga la DB.

## En el código

```python
def update(key, value):
    DB[key] = value
    cache.pop(key, None)   # ← la única línea que cambia
```

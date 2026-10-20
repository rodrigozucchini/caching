# Caché sin límite

## El problema

Se usa un `dict` como caché de búsquedas. Cada búsqueda distinta agrega una
entrada y nada se borra nunca. La memoria crece hasta que el proceso muere.

```
 entradas
 100.000 │                  ╱
         │            ╱
         │      ╱             ← crece con cada búsqueda nueva
       0 └───────────────────► búsquedas
```

## Por qué pasa

Un `dict` no tiene tamaño máximo. Si las claves casi no se repiten
(búsquedas de texto libre, ids de request), cada request agrega algo nuevo y
la mayoría de esas entradas no se vuelve a usar nunca.

## La solución

Ponerle un **tamaño máximo** al caché. Cuando está lleno y llega algo nuevo,
primero se borra la entrada que hace más tiempo nadie usa (política LRU):
además del diccionario, una lista `order` guarda las claves por orden de uso.

```
 entradas
         │
    1000 │   ┌─────────────────   ← nunca pasa de 1000
         │  ╱
       0 └─────────────────────► búsquedas
```

## Por qué funciona

La memoria queda acotada: nunca hay más de 1000 entradas, pase lo que pase.
Y se borra lo menos útil: lo que se usó hace poco probablemente se vuelva a
usar, lo que nadie pidió en mucho tiempo probablemente no. (Ver
`implementations/07_lru.md` para el detalle de cómo elige qué borrar.)

## En el código

```python
if len(cache) >= MAX_SIZE:   # ← antes de agregar, si está lleno...
    oldest = order.pop(0)    #    ...se saca la menos usada
    del cache[oldest]
```

En Python, `@functools.lru_cache(maxsize=1000)` hace todo esto en una línea.

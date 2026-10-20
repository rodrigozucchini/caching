# Memoización

## Qué problema resuelve

Una función cara (un cálculo pesado, leer y parsear un archivo de
configuración) se llama muchas veces con los mismos argumentos, y cada vez
hace todo el trabajo de nuevo para llegar al mismo resultado.

## Cómo lo resuelve

Un diccionario `memo` donde la **clave son los argumentos** y el **valor es
el resultado**. Antes de calcular se mira si ya está.

```
 slow_square(4)  1ra vez                slow_square(4)  2da vez

 ¿4 está en memo? no                    ¿4 está en memo? sí
        │                                       │
        ▼                                       ▼
 calcula (0.5s)                         devuelve memo[4] = 16
        │                               (0.0000s, sin calcular)
        ▼
 memo[4] = 16
```

## Por qué así

- Es lo más simple posible: un diccionario y un `if`.
- El trabajo caro se hace una sola vez por cada combinación de argumentos.
- En Python ya viene hecho como `@functools.lru_cache`, que además le pone un
  límite de tamaño. Por dentro es esta misma idea.

## Cuándo usarla y cuándo no

- **Sí:** funciones puras (mismo input → mismo output), configuración que se
  lee una sola vez al arrancar, cálculos repetidos.
- **No:** datos que cambian (usuarios, precios): `memo` nunca se borra, así
  que seguiría devolviendo el valor viejo. Para eso está el 02 (TTL) o el 04.
- **Cuidado:** si los argumentos casi nunca se repiten, `memo` crece sin
  límite (ver `errors/06_unbounded_cache.md`).

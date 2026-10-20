# Caching: implementaciones y errores

Los **7 tipos de caching más usados** y los **7 errores más comunes**.
Cada archivo es independiente, corto y se ejecuta solo:

```bash
python implementations/04_cache_aside.py
python errors/02_cache_stampede_error.py
python errors/02_cache_stampede_fix.py
```

Los conceptos y el código son independientes del lenguaje: se usan
diccionarios, listas y locks, que existen en cualquier lenguaje. Cuando se
usa algo propio de Python, el comentario dice qué es y cómo se haría sin eso.

Todo es Python puro, salvo `implementations/03_distributed_redis.py`, que usa
`fakeredis` (Redis en memoria, sin Docker): `pip install fakeredis`.

## Estructura

```
caching/
├── README.md
├── implementations/
│   ├── NN_nombre.py             el código
│   └── NN_nombre.md             explicación + diagrama
└── errors/
    ├── NN_nombre_error.py       muestra el error
    ├── NN_nombre_fix.py         la solución
    └── NN_nombre.md             explicación + diagramas del error y del fix
```

Conviene leer primero el `.md` y después el código. Siempre tiene las mismas
secciones:

| `.md` de | Secciones |
|----------|-----------|
| implementación | Qué problema resuelve · Cómo lo resuelve (diagrama) · Por qué así · Cuándo usarla y cuándo no |
| error | El problema (diagrama) · Por qué pasa · La solución (diagrama) · Por qué funciona · En el código |

Cada archivo empieza con un docstring con siempre las mismas secciones:

| Archivo | Secciones |
|---------|-----------|
| `implementations/*` y `*_fix.py` | **Problema** · **Qué uso** · **Solución** · **Por qué** |
| `*_error.py` | **Problema** · **Qué vas a ver** |

Debajo va el código mínimo para mostrarlo. La "DB" es un dict, con
`time.sleep` donde importa que sea lenta y un contador `db_reads` para ver
cuántas veces se consultó.

## Implementaciones

| # | Archivo | Problema que resuelve | Qué usa |
|---|---------|-----------------------|---------|
| 01 | `01_memoization` | función cara recalcula lo mismo | dict argumentos → resultado |
| 02 | `02_in_memory_ttl` | el dato cambia y el caché no vence | dict con vencimiento |
| 03 | `03_distributed_redis` | varias instancias, cada una con su caché | Redis compartido |
| 04 | `04_cache_aside` | DB lenta para lecturas repetidas (**la más usada**) | leer caché → DB; escribir DB → borrar |
| 05 | `05_write_through` | lo recién escrito no está en caché | escribir DB + caché juntos |
| 06 | `06_write_behind` | demasiadas escrituras a la DB | escribir en caché, volcar con `flush()` |
| 07 | `07_lru` | ¿qué borrar cuando el caché se llena? | dict + lista por orden de uso |

## Errores

| # | Error | Qué pasa | Fix |
|---|-------|----------|-----|
| 01 | `stale_data` | se actualiza la DB y el caché no | borrar la clave al escribir |
| 02 | `cache_stampede` | 20 requests simultáneos → 20 consultas | lock (uno solo va a la DB) |
| 03 | `cache_avalanche` | 1000 claves vencen en el mismo segundo | TTL + número aleatorio (jitter) |
| 04 | `cache_penetration` | ids inexistentes siempre van a la DB | cachear el "no existe" |
| 05 | `bad_cache_key` | la clave no tiene `user_id` → fuga de datos | incluir el `user_id` en la clave |
| 06 | `unbounded_cache` | el caché crece sin límite | tamaño máximo + borrar la menos usada |
| 07 | `mutable_cached_object` | modificar lo cacheado lo cambia para todos | devolver una copia |

## Orden de estudio sugerido

1. impl 01, 02, 04 → error 01
2. impl 07 → error 06
3. errores 05, 07
4. errores 02, 03, 04
5. impl 03, 05, 06

Para cada error: ejecutar el `_error.py`, pensar la solución, y recién
después abrir el `_fix.py`.

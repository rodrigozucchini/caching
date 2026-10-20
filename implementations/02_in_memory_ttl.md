# Caché en memoria con TTL

## Qué problema resuelve

Hay datos que cambian con el tiempo (una cotización, una configuración). Con
la memoización (01) quedarían guardados para siempre con el valor viejo.

## Cómo lo resuelve

Junto con el valor se guarda **cuándo vence**. Al leer, si ya venció, se
borra y se responde como si no estuviera, así que se vuelve a buscar el dato
actualizado.

```
 cache = { "dolar": (1000, vence = ahora + 1s) }

 tiempo ──────────────────────────────────────────────────►
        │ cache_set        │ +1s
        │◄──── válido ────►│◄───────── vencido ──────────
        │                  │
   cache_get → 1000        │   cache_get → venció → lo borra → None
```

## Por qué así

- Garantiza que un dato nunca tenga más antigüedad que el TTL.
- Es solo un dict: no necesita nada instalado.
- Usa `time.monotonic()` en vez de `time.time()` porque no salta si alguien
  cambia la hora del sistema.

## Cuándo usarla y cuándo no

- **Sí:** una sola instancia de la app, datos que pueden estar un poco
  desactualizados (segundos o minutos).
- **No:** varias instancias de la app (cada una tendría su copia) → 03 Redis.

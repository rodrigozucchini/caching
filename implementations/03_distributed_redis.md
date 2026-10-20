# Caché distribuido (Redis)

## Qué problema resuelve

En producción la app corre en varias instancias (varios servidores o
contenedores). Si cada una tiene su caché en memoria, cada una consulta la
DB por lo mismo y pueden tener valores distintos entre sí.

## Cómo lo resuelve

El caché sale de la app y pasa a un servidor aparte (Redis) al que todas las
instancias se conectan. Lo que guarda una le sirve a todas.

```
  ┌───────┐  1. GET user:1 → no está    ┌─────────────┐
  │ app A │────────────────────────────►│             │
  │       │  3. SET user:1 "Ana" EX 60  │    Redis    │
  │       │────────────────────────────►│             │
  └───┬───┘                             │ user:1: Ana │
      │ 2. consulta                     │             │
      ▼                                 │             │
  ┌───────┐                             │             │
  │  DB   │   ┌───────┐ 4. GET user:1   │             │
  └───────┘   │ app B │◄────────────────│             │
              └───────┘   → "Ana"       └─────────────┘
              no toca la DB
```

## Por qué así

- **Un solo caché compartido:** la DB se consulta una vez, no una por instancia.
- **Mismo valor para todos:** no hay instancias con datos distintos.
- **TTL incluido:** `SET clave valor EX 60` vence solo a los 60s.
- **Sobrevive** a reinicios y deploys de la app.

## Cuándo usarla y cuándo no

- **Sí:** casi siempre que la app tiene más de una instancia.
- **Costo:** cada acceso es un viaje por red (~1ms) en vez de nanosegundos, y
  el valor hay que convertirlo a texto (JSON) para guardarlo.

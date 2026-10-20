# Write-behind (write-back)

## Qué problema resuelve

Hay muchísimas escrituras sobre los mismos datos (contador de vistas, likes)
y escribir cada una en la DB la satura.

## Cómo lo resuelve

Las escrituras van **solo al caché**, que anota qué claves cambiaron
(`dirty`). Cada tanto, `flush()` lleva a la DB el valor final de cada clave
modificada, en una sola escritura.

```
 increment() x1000                    flush() cada N segundos
       │                                     │
       ▼                                     ▼
 ┌─────────────────┐                 ┌──────────────┐          ┌──────────┐
 │ caché           │                 │ para cada    │  1 sola  │ DB       │
 │ views:home=1000 │────────────────►│ clave dirty  │─────────►│ views=   │
 │ dirty={home}    │                 └──────────────┘ escritura│   1000   │
 └─────────────────┘                                           └──────────┘
 instantáneo, sin tocar la DB
```

## Por qué así

- Las escrituras son instantáneas: solo tocan memoria.
- 1000 cambios sobre la misma clave terminan en **1** escritura a la DB:
  solo importa el valor final.

## Cuándo usarla y cuándo no

- **Sí:** contadores, métricas, datos donde perder unos segundos de cambios
  es aceptable.
- **No:** dinero, pedidos, nada que no se pueda perder. Si la app se cae
  antes del `flush()`, los cambios pendientes se pierden.

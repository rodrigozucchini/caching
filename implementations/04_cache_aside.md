# Cache-aside (la estrategia más usada)

## Qué problema resuelve

La DB es lenta y se leen los mismos datos una y otra vez.

## Cómo lo resuelve

La app pone el caché "al costado" de la DB y lo maneja ella misma:

```
 LECTURA                                 ESCRITURA

 app ──► ¿está en caché?                 app ──► escribe en la DB
          │                                       │
          ├─ sí ─► lo devuelve                    ▼
          │                              app ──► BORRA la clave del caché
          └─ no ─► lo lee de la DB
                   lo guarda en caché    la próxima lectura no la encuentra
                   lo devuelve           y trae el valor nuevo de la DB
```

## Por qué así

- **Solo cachea lo que se lee:** no llena el caché con datos que nadie pide.
- **Tolerante a fallos:** si el caché se cae, la app sigue funcionando
  leyendo de la DB (más lenta, pero funciona).
- **Al escribir se borra en vez de actualizar:** borrar no depende del
  orden en que lleguen dos escrituras simultáneas (ver
  `errors/01_stale_data.md`).

## Cuándo usarla y cuándo no

- **Sí:** el caso general, apps con muchas más lecturas que escrituras.
- **Costo:** la primera lectura de cada dato (y la primera después de cada
  escritura) siempre va a la DB.

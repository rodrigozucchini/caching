# Write-through

## Qué problema resuelve

Con cache-aside, después de escribir se borra la clave, así que la primera
lectura siempre va a la DB. Si lo que se escribe se lee enseguida (carrito,
sesión, perfil), esa lectura es lenta siempre.

## Cómo lo resuelve

Toda escritura guarda el dato **en la DB y en el caché** en la misma
operación.

```
         write("cart:7", ["libro"])
                   │
          ┌────────┴────────┐
          ▼                 ▼
     ┌─────────┐       ┌─────────┐
     │   DB    │       │  caché  │
     └─────────┘       └────┬────┘
                            │
     read("cart:7") ◄───────┘  ya está, desde la primera lectura
```

## Por qué así

- Lo recién escrito ya está en caché, sin un primer miss.
- El caché siempre tiene el mismo valor que la DB.

## Cuándo usarla y cuándo no

- **Sí:** datos que se escriben y se leen enseguida.
- **Costo:** cada escritura espera a la DB y al caché. Y se cachea todo lo
  que se escribe, aunque nadie lo lea después.

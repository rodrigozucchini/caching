# Cache stampede

## El problema

Una clave muy pedida no está en caché (venció, o la app recién arrancó) y en
ese momento llegan muchos requests a la vez. Todos van a la DB por el mismo
dato.

```
 req 1 ──► ¿está? no ──► DB ┐
 req 2 ──► ¿está? no ──► DB ├── 20 consultas idénticas y pesadas
 ...                        │   a la vez → la DB se satura
 req 20 ─► ¿está? no ──► DB ┘
```

## Por qué pasa

La consulta a la DB tarda (0.5s). Durante ese tiempo el caché sigue vacío,
porque el valor se guarda recién cuando la consulta termina. Todos los
requests que llegan en ese medio segundo ven "no está" y también van a la DB.

## La solución

Un **lock**: solo un request puede ir a la DB por la clave. Los demás esperan,
y cuando les toca vuelven a mirar el caché.

```
 req 1  ──► ¿está? no ──► toma el lock ──► DB ──► guarda ──► suelta el lock
 req 2  ──► ¿está? no ──► espera el lock ───────────────────► ¿está? sí ✓
 ...
 req 20 ──► ¿está? no ──► espera el lock ───────────────────► ¿está? sí ✓

                          1 sola consulta a la DB
```

## Por qué funciona

- El lock hace que la consulta a la DB la haga **uno solo a la vez**.
- El segundo `if key not in cache` dentro del lock es la clave: los que
  estaban esperando, al entrar, encuentran el valor que dejó el primero y no
  consultan la DB.
- Sin ese segundo chequeo, el lock solo los pondría en fila y cada uno haría
  igual su consulta.

Con varias instancias de la app el lock de Python no alcanza (cada proceso
tiene el suyo); se usa un lock en Redis: `SET lock:clave 1 NX EX 5`.

## En el código

```python
def get(key):
    if key in cache:
        return cache[key]
    with lock:                    # ← uno a la vez
        if key not in cache:      # ← volver a mirar: quizás otro ya lo cargó
            cache[key] = db_get(key)
    return cache[key]
```

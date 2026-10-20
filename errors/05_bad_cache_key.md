# Clave de caché mal construida

## El problema

El dashboard es distinto para cada usuario, pero la clave del caché es
siempre `"dashboard"`. El primero que entra deja **sus** datos en caché y
todos los demás los ven.

```
 Ana  (user 1) ──► "dashboard" ──► no está ──► DB ──► guarda "Ana: $5000"
 Beto (user 2) ──► "dashboard" ──► está    ──► devuelve "Ana: $5000"   ✗
```

## Por qué pasa

El caché solo sabe lo que le dice la clave. Si la clave no incluye el
usuario, para el caché Ana y Beto están pidiendo exactamente lo mismo. Es una
fuga de datos: un usuario ve información privada de otro.

## La solución

Incluir en la clave **todo lo que cambia el resultado**, en este caso el
`user_id`.

```
 Ana  (user 1) ──► "dashboard:1" ──► "Ana: $5000"   ✓
 Beto (user 2) ──► "dashboard:2" ──► "Beto: $20"    ✓
```

## Por qué funciona

Cada usuario tiene su propia entrada en el caché, así que es imposible que a
uno le llegue lo de otro. La regla general: si el resultado depende de algo
(usuario, idioma, moneda, página, filtros), ese algo va en la clave.

El `:` separa los valores para que no se mezclen: sin separador, la orden 1
línea 23 (`"123"`) y la orden 12 línea 3 (`"123"`) darían la misma clave.

## En el código

```python
key = f"dashboard:{user_id}"   # ← en vez de key = "dashboard"
```

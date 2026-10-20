# LRU (Least Recently Used)

## Qué problema resuelve

La memoria es limitada. Cuando el caché se llena y hay que guardar algo
nuevo, hay que decidir qué borrar.

## Cómo lo resuelve

Borra la clave que hace **más tiempo que nadie usa**. Para saber cuál es,
además del diccionario con los valores se mantiene una lista `order` con las
claves ordenadas por último uso: cada vez que se usa una, pasa al final; la
del principio es siempre la que se borra.

```
 capacidad = 3        menos reciente ◄─────────► más reciente

 put A               [ A ]
 put B               [ A | B ]
 put C               [ A | B | C ]
 get A               [ B | C | A ]       A se usó → pasa al final
 put D               [ B | C | A | D ]   se pasó de 3
                       │
                       └─► se borra B    [ C | A | D ]
```

## Por qué así

- **Lo que se usó hace poco suele volver a usarse pronto**, y lo que nadie
  pide hace rato, probablemente no. Así se conserva lo útil.
- Es la política por defecto en casi todos los cachés (Redis: `allkeys-lru`).
- **Sobre la lista:** mover o borrar una clave de una lista común obliga a
  recorrerla, lo que es lento con muchas claves. Las implementaciones reales
  usan una lista doblemente enlazada + diccionario, que hace todo sin
  recorrer nada. En Python esa estructura ya existe: `collections.OrderedDict`.

## Cuándo usarla y cuándo no

- **Sí:** es la política por defecto y funciona bien casi siempre.
- **Punto débil:** si alguien recorre muchas claves una sola vez (un reporte
  que lee todo), empuja fuera a las que se usan siempre. Para eso existe
  LFU, que borra la menos usada en total.

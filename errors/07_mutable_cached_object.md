# Objetos mutables en caché

## El problema

El caché devuelve una **lista** de permisos. Un request le agrega `"write"`
para usarla él solo... pero modifica la lista que está guardada en el caché.
Desde ese momento todos los viewers pueden escribir.

```
 caché: viewer ─► ["read"]
                     ▲
                     │ es el MISMO objeto, no una copia
 request: perms ─────┘
   perms.append("write")

 caché: viewer ─► ["read", "write"]   ✗ para todos
```

## Por qué pasa

Un caché en memoria no devuelve una copia: devuelve una **referencia** al
objeto guardado (un "puntero" al mismo lugar de memoria). Quien recibe la
lista y la modifica está modificando la única lista que existe, la del caché.

No pasa con un caché externo como Redis: ahí cada lectura crea un objeto
nuevo a partir del texto guardado.

## La solución

El caché guarda el original y a cada lector le entrega una **copia**.

```
 caché: viewer ─► ["read"]        ← el original nunca sale del caché
                     │
                     │ copia
                     ▼
 request: perms ─► ["read"]       ← un objeto distinto
   perms.append("write")
                     ▼
          perms ─► ["read", "write"]   solo en la copia

 caché: viewer ─► ["read"]   ✓ intacto
```

## Por qué funciona

Cada lector recibe su propio objeto y puede modificarlo sin afectar a nadie,
porque el original nunca se entrega.

Dos detalles:
- **Copia profunda:** si el objeto tiene otros objetos adentro (una lista de
  diccionarios, por ejemplo), hay que copiar también esos, o seguirían siendo
  compartidos. En Python: `copy.deepcopy`.
- **Alternativa: valores inmutables.** Si se guardan datos que no se pueden
  modificar (en Python, un `tuple` en vez de una lista), no hace falta
  copiar: si alguien intenta cambiarlo da error en ese momento. Es más barato
  porque no copia en cada lectura.

## En el código

```python
return list(cache[role])   # ← una copia, en vez de return cache[role]
```

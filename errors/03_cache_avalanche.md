# Cache avalanche

## El problema

Se cargan 1000 claves al mismo tiempo (al arrancar la app, o un proceso
nocturno) y todas con TTL de 60s. Todas vencen en el mismo segundo, y en ese
segundo las 1000 van a la DB.

```
 consultas a la DB
  1000 │            █
       │            █
       │            █      ← todo de golpe en el segundo 60
     0 └────────────┴────► segundos
                    60
```

## Por qué pasa

`vencimiento = momento_de_carga + TTL`. Si todas se cargaron en el mismo
momento y tienen el mismo TTL, la cuenta da el mismo resultado para todas.

## La solución

Sumarle al TTL un **valor aleatorio** (jitter), por ejemplo entre -10 y +10
segundos.

```
 consultas a la DB
  1000 │
       │
   100 │   ▂▃▅▆▅▆▅▅▆▅▆▃▅▆▅▃▂     ← repartidas entre el segundo 50 y el 70
     0 └───┴─────────────────┴─► segundos
           50                70
```

## Por qué funciona

Cada clave recibe un TTL un poco distinto, así que vencen en momentos
distintos. La DB recibe la misma cantidad total de consultas, pero repartidas
en 20 segundos en vez de todas en 1. Que una clave dure 52s o 67s en vez de
60s no le importa a nadie.

## En el código

```python
ttl = 60 + random.uniform(-10, 10)   # ← en vez de ttl = 60
```

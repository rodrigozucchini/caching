# Caching: qué es, para qué sirve, y los errores que todos cometemos

## ¿Qué es el caching?

El **caching** consiste en guardar una copia de un dato en un lugar más rápido de acceder que su origen, para no tener que ir a buscarlo cada vez.

El origen suele ser algo lento o caro: una base de datos, una API externa, un cálculo pesado o un archivo en disco. El caché suele ser la memoria RAM o un servidor dedicado como Redis. La diferencia de velocidad es enorme: leer de memoria tarda nanosegundos, una consulta a una base de datos tarda milisegundos y una API externa puede tardar cientos de milisegundos.

La idea es simple:

1. Pedís un dato.
2. Si está en el caché (un **hit**), lo devolvés al instante.
3. Si no está (un **miss**), lo buscás en el origen, lo guardás en el caché y lo devolvés.

La próxima vez que alguien pida ese dato, ya va a estar.

## ¿Para qué sirve?

- **Velocidad:** las respuestas pasan de segundos o milisegundos a casi instantáneas.
- **Menos carga en la base de datos:** si 10.000 usuarios piden el mismo producto, la DB se consulta una vez y no 10.000.
- **Menos costos:** menos consultas a APIs pagas, menos CPU y servidores de base de datos más chicos.
- **Resiliencia:** si el origen está lento o caído por un momento, el caché puede seguir respondiendo.

## El precio: ahora hay dos copias del dato

El caching no es gratis. Desde el momento en que cacheás algo, el mismo dato existe en dos lugares, y mantenerlos sincronizados es el gran desafío. Como dice la frase famosa de Phil Karlton:

> "Hay solo dos cosas difíciles en ciencias de la computación: la invalidación de caché y ponerle nombre a las cosas."

Casi todos los errores de caching vienen de ahí: el caché y el origen dejan de estar de acuerdo, el caché crece sin control o el caché deja de proteger al origen justo cuando más se lo necesita.

## Tipos de caching

| # | Tipo | Problema | Cómo funciona | Cuidado |
|---|------|----------|---------------|---------|
| 1 | **Memoización** | Una función cara recalcula lo mismo | Diccionario argumentos → resultado | No vence: solo para datos que no cambian |
| 2 | **En memoria con TTL** | El dato cambia con el tiempo | Cada valor guarda cuándo vence | Cada instancia tiene su copia |
| 3 | **Distribuido (Redis)** | Varias instancias, cada una con su caché | Un caché compartido por todas | Cada acceso es un viaje por red |
| 4 | **Cache-aside** | DB lenta para lecturas repetidas | Leer: caché → DB. Escribir: DB → borrar del caché | La primera lectura siempre va a la DB |
| 5 | **Write-through** | Lo recién escrito no está en caché | Escribir en DB y caché a la vez | Escrituras más lentas |
| 6 | **Write-behind** | Demasiadas escrituras a la DB | Escribir en caché y volcar a la DB cada tanto | Si se cae la app, se pierden cambios |
| 7 | **LRU** | El caché se llena: ¿qué borrar? | Borrar la clave que hace más tiempo nadie usa | Un recorrido masivo expulsa las populares |

### ¿Qué estrategia elegir?

| Situación | Estrategia |
|-----------|------------|
| Caso general, mucha lectura | Cache-aside |
| Lo que se escribe se lee enseguida | Write-through |
| Muchísimas escrituras y se tolera perder algunas | Write-behind |

## Errores más comunes

| # | Error | Qué pasa | Solución |
|---|-------|----------|----------|
| 1 | **Stale data** | La DB cambia y el caché sigue con el valor viejo | Borrar la clave del caché al escribir |
| 2 | **Cache stampede** | Vence una clave popular y todos van a la DB a la vez | Lock: solo uno va a la DB, los demás esperan |
| 3 | **Cache avalanche** | Muchas claves con el mismo TTL vencen juntas | Sumar un valor aleatorio al TTL (jitter) |
| 4 | **Cache penetration** | Las claves inexistentes nunca se cachean | Cachear también el "no existe" |
| 5 | **Clave mal construida** | Un usuario ve los datos de otro | Incluir en la clave todo lo que cambia el resultado |
| 6 | **Caché sin límite** | La memoria crece hasta romper | Tamaño máximo + borrar lo menos usado (LRU) |
| 7 | **Objetos mutables** | Modificar lo cacheado lo cambia para todos | Devolver una copia o valores inmutables |

## Conclusión

Un caché bien usado hace que una app sea rápida y barata. Mal usado, sirve datos viejos, filtra información entre usuarios o tumba la base de datos justo en el pico de tráfico.

Antes de cachear algo, conviene hacerse cuatro preguntas:

1. **¿Cuándo deja de ser válido este dato?** Eso define el TTL y la invalidación.
2. **¿De qué depende el resultado?** Todo eso tiene que ir en la clave.
3. **¿Qué pasa si muchos lo piden a la vez cuando no está?** Ahí aparece el stampede.
4. **¿Cuánto puede crecer?** Eso define el límite y la política de eviction.

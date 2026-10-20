"""
Write-behind (write-back)

Problema:  hay muchísimas escrituras (contador de vistas, likes) y escribir
           cada una en la DB la satura.
Qué uso:   un dict como caché + un set con las claves modificadas.
Solución:  escribir solo en el caché; cada cierto tiempo flush() vuelca a la
           DB lo modificado en una sola escritura por clave.
Por qué:   escrituras instantáneas y 1000 cambios sobre la misma clave se
           convierten en 1 escritura a la DB.
Costo:     si la app se cae antes del flush, esos cambios se pierden.

Ejecutar: python implementations/06_write_behind.py
"""
DB = {"views:home": 0}     # la "base de datos"
cache = {"views:home": 0}  # el caché, que es donde se escribe
dirty = set()              # claves que cambiaron en el caché y todavía no se guardaron en la DB
db_writes = 0              # cuántas escrituras llegaron a la DB


def increment(key):
    cache[key] += 1  # solo se cambia el caché (instantáneo, no toca la DB)
    dirty.add(key)   # se anota que esta clave está pendiente de guardar.
                     # Es un set: aunque se agregue 1000 veces, queda una sola vez.


def flush():  # en una app real lo llama un timer cada N segundos
    global db_writes
    # Por cada clave pendiente se escribe en la DB su valor FINAL (una sola vez).
    for key in dirty:
        DB[key] = cache[key]
        db_writes += 1
    dirty.clear()  # ya está todo guardado, no queda nada pendiente


# 1000 incrementos: todos en memoria, la DB no se entera todavía
for _ in range(1000):
    increment("views:home")
print("antes del flush -> DB:", DB["views:home"])  # 0

# flush: 1000 cambios en el caché → 1 sola escritura con el valor 1000
flush()
print("después del flush -> DB:", DB["views:home"], f"con {db_writes} escritura")

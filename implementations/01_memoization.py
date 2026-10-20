"""
Memoización

Problema:  una función cara se llama muchas veces con los mismos argumentos
           y recalcula siempre lo mismo.
Qué uso:   un diccionario donde la clave son los argumentos y el valor es
           el resultado.
Solución:  antes de calcular, buscar los argumentos en el diccionario; si
           están, devolver el resultado guardado; si no, calcular y guardar.
Por qué:   el trabajo caro se hace una sola vez por cada combinación de
           argumentos. Sirve solo para funciones puras: mismo input -> mismo
           output, y sin depender de nada que cambie (DB, hora, archivos).

Ejecutar: python implementations/01_memoization.py
"""
import time

memo = {}  # argumentos -> resultado ya calculado


def slow_square(x):
    if x in memo:       # ¿ya se calculó con este argumento?
        return memo[x]  # sí: se devuelve sin hacer el trabajo

    time.sleep(0.5)     # no: se hace el cálculo caro (simulado con 0.5s)
    result = x * x
    memo[x] = result    # se guarda para la próxima vez
    return result

# Nota: Python trae esto hecho como decorador (@functools.lru_cache), que
# además le pone un límite de tamaño. Por dentro hace lo mismo que arriba.


start = time.perf_counter()  # perf_counter: un cronómetro para medir cuánto tarda
slow_square(4)               # 4 no está en memo → calcula (0.5s) y guarda memo[4] = 16
print(f"1ra llamada: {time.perf_counter() - start:.2f}s")

start = time.perf_counter()
slow_square(4)               # 4 está en memo → devuelve 16 al instante
print(f"2da llamada: {time.perf_counter() - start:.4f}s (desde memo)")

print("memo:", memo)

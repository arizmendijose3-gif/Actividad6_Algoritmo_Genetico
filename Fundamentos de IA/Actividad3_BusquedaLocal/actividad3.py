# ============================================================
# ACTIVIDAD 3: ALGORITMOS DE BUSQUEDA LOCAL
# Hill Climbing y Simulated Annealing
#
# Asignatura: Fundamentos de Inteligencia Artificial
# Universidad Politecnica de Atlautla
#
# Objetivo:
# Minimizar una funcion matematica y comparar los resultados
# de dos algoritmos de busqueda local.
# ============================================================

import random
import math
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# 1. DEFINIR LA FUNCION OBJETIVO
# ------------------------------------------------------------

def funcion_objetivo(x):
    """
    Calcula el costo de una solucion x.
    El objetivo es minimizar el resultado.
    """
    return (x ** 2 - 1) ** 2 + 0.15 * x


# Limites del espacio de busqueda
LIMITE_INFERIOR = -2.0
LIMITE_SUPERIOR = 2.0


# ------------------------------------------------------------
# 2. ALGORITMO HILL CLIMBING
# ------------------------------------------------------------

def hill_climbing(
    inicio=0.8,
    paso=0.02,
    iteraciones=2000,
    semilla=42
):
    """
    Busca una solucion de menor costo.

    Solamente acepta movimientos que mejoran
    la solucion actual.
    """

    # Generador aleatorio reproducible
    generador = random.Random(semilla)

    # Solucion inicial
    actual = inicio

    # Registrar el costo inicial
    costo_actual = funcion_objetivo(actual)

    # Guardar la mejor solucion encontrada
    mejor = actual
    mejor_costo = costo_actual

    # Historial de convergencia
    historial = []

    # Repetir el proceso
    for _ in range(iteraciones):

        # Elegir un movimiento positivo o negativo
        movimiento = generador.choice([-paso, paso])

        # Crear una solucion vecina
        vecino = actual + movimiento

        # Mantener la solucion dentro de los limites
        vecino = max(
            LIMITE_INFERIOR,
            min(LIMITE_SUPERIOR, vecino)
        )

        # Calcular el costo del vecino
        costo_vecino = funcion_objetivo(vecino)

        # Aceptar solamente si mejora el costo
        if costo_vecino < costo_actual:

            actual = vecino
            costo_actual = costo_vecino

        # Actualizar la mejor solucion encontrada
        if costo_actual < mejor_costo:

            mejor = actual
            mejor_costo = costo_actual

        # Registrar el mejor costo de esta iteracion
        historial.append(mejor_costo)

    return mejor, mejor_costo, historial


# ------------------------------------------------------------
# 3. ALGORITMO SIMULATED ANNEALING
# ------------------------------------------------------------

def simulated_annealing(
    inicio=0.8,
    desviacion=0.35,
    temperatura_inicial=2.0,
    enfriamiento=0.998,
    iteraciones=3000,
    semilla=1
):
    """
    Busca una solucion de menor costo.

    Puede aceptar temporalmente soluciones peores
    dependiendo de la temperatura.
    """

    # Generador aleatorio reproducible
    generador = random.Random(semilla)

    # Solucion inicial
    actual = inicio

    # Costo de la solucion actual
    costo_actual = funcion_objetivo(actual)

    # Registrar la mejor solucion encontrada
    mejor = actual
    mejor_costo = costo_actual

    # Temperatura inicial
    temperatura = temperatura_inicial

    # Historial de convergencia
    historial = []

    # Ejecutar las iteraciones
    for _ in range(iteraciones):

        # Generar una solucion vecina
        vecino = actual + generador.gauss(
            0,
            desviacion
        )

        # Respetar los limites del problema
        vecino = max(
            LIMITE_INFERIOR,
            min(LIMITE_SUPERIOR, vecino)
        )

        # Calcular el costo de la nueva solucion
        costo_vecino = funcion_objetivo(vecino)

        # Diferencia de costo
        diferencia = costo_vecino - costo_actual

        # Aceptar siempre una mejora
        if diferencia < 0:

            aceptar = True

        else:

            # Calcular la probabilidad de aceptar
            # una solucion que empeora el costo.
            probabilidad = math.exp(
                -diferencia / max(temperatura, 1e-12)
            )

            aceptar = (
                generador.random() < probabilidad
            )

        # Actualizar la solucion actual
        if aceptar:

            actual = vecino
            costo_actual = costo_vecino

        # Conservar la mejor solucion encontrada
        if costo_actual < mejor_costo:

            mejor = actual
            mejor_costo = costo_actual

        # Registrar el mejor costo
        historial.append(mejor_costo)

        # Reducir la temperatura
        temperatura *= enfriamiento

    return mejor, mejor_costo, historial


# ------------------------------------------------------------
# 4. EJECUTAR LOS DOS ALGORITMOS
# ------------------------------------------------------------

print("=" * 60)
print("ACTIVIDAD 3: BUSQUEDA LOCAL")
print("=" * 60)

# Ejecutar Hill Climbing
mejor_hc, costo_hc, historial_hc = hill_climbing()

# Ejecutar Simulated Annealing
mejor_sa, costo_sa, historial_sa = simulated_annealing()


# ------------------------------------------------------------
# 5. MOSTRAR LOS RESULTADOS
# ------------------------------------------------------------

print("\nRESULTADOS DE HILL CLIMBING")

print("Mejor valor de x:", round(mejor_hc, 6))
print("Costo minimo encontrado:", round(costo_hc, 6))


print("\nRESULTADOS DE SIMULATED ANNEALING")

print("Mejor valor de x:", round(mejor_sa, 6))
print("Costo minimo encontrado:", round(costo_sa, 6))


# Comparar los resultados
print("\nCOMPARACION")

if costo_sa < costo_hc:

    print(
        "Simulated Annealing encontro una solucion "
        "de menor costo en esta ejecucion."
    )

elif costo_hc < costo_sa:

    print(
        "Hill Climbing encontro una solucion "
        "de menor costo en esta ejecucion."
    )

else:

    print("Ambos algoritmos encontraron el mismo costo.")


# ------------------------------------------------------------
# 6. GRAFICA DE LA FUNCION OBJETIVO
# ------------------------------------------------------------

# Generar valores de x sin utilizar bibliotecas adicionales
valores_x = [
    LIMITE_INFERIOR + i * 0.01
    for i in range(401)
]

# Evaluar la funcion para cada valor
valores_y = [
    funcion_objetivo(x)
    for x in valores_x
]

plt.figure(figsize=(10, 6))

plt.plot(
    valores_x,
    valores_y,
    label="Funcion objetivo"
)

# Marcar la solucion de Hill Climbing
plt.scatter(
    [mejor_hc],
    [costo_hc],
    label="Hill Climbing"
)

# Marcar la solucion de Simulated Annealing
plt.scatter(
    [mejor_sa],
    [costo_sa],
    label="Simulated Annealing"
)

plt.title("Funcion objetivo y soluciones encontradas")
plt.xlabel("Valor de x")
plt.ylabel("Costo f(x)")
plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig(
    "grafica_funcion.png",
    dpi=200,
    bbox_inches="tight"
)

plt.show()
plt.close()


# ------------------------------------------------------------
# 7. GRAFICA DE CONVERGENCIA
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    range(1, len(historial_hc) + 1),
    historial_hc,
    label="Hill Climbing"
)

plt.plot(
    range(1, len(historial_sa) + 1),
    historial_sa,
    label="Simulated Annealing"
)

plt.title("Comparacion de convergencia")
plt.xlabel("Iteracion")
plt.ylabel("Mejor costo encontrado")
plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig(
    "grafica_convergencia.png",
    dpi=200,
    bbox_inches="tight"
)

plt.show()
plt.close()


# ------------------------------------------------------------
# 8. GUARDAR LOS RESULTADOS EN UN ARCHIVO DE TEXTO
# ------------------------------------------------------------

with open(
    "resultados.txt",
    "w",
    encoding="utf-8"
) as archivo:

    archivo.write("RESULTADOS DE LA ACTIVIDAD 3\n\n")

    archivo.write("HILL CLIMBING\n")
    archivo.write(
        f"Mejor x: {mejor_hc:.6f}\n"
    )
    archivo.write(
        f"Mejor costo: {costo_hc:.6f}\n\n"
    )

    archivo.write("SIMULATED ANNEALING\n")
    archivo.write(
        f"Mejor x: {mejor_sa:.6f}\n"
    )
    archivo.write(
        f"Mejor costo: {costo_sa:.6f}\n"
    )

print("\nArchivos generados correctamente:")
print("- grafica_funcion.png")
print("- grafica_convergencia.png")
print("- resultados.txt")

print("\nEjecucion finalizada.")
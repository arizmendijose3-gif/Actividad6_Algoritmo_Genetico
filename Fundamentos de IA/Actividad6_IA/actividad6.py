import random
import math
import matplotlib.pyplot as plt

from deap import base, creator, tools, algorithms

# ==================================================
# ACTIVIDAD 6: ALGORITMO GENETICO PARA EL PROBLEMA TSP
# ==================================================

# Fijar una semilla permite repetir los experimentos
# con los mismos datos y obtener resultados reproducibles.
random.seed(42)

# Coordenadas de las ciudades: (X, Y)
ciudades = {
    "Ciudad A": (0, 0),
    "Ciudad B": (2, 6),
    "Ciudad C": (5, 8),
    "Ciudad D": (8, 7),
    "Ciudad E": (10, 3),
    "Ciudad F": (7, 0),
    "Ciudad G": (4, 2),
    "Ciudad H": (1, 4)
}

nombres_ciudades = list(ciudades.keys())
numero_ciudades = len(nombres_ciudades)


# ==================================================
# CALCULAR LA DISTANCIA ENTRE DOS CIUDADES
# ==================================================

def distancia(ciudad1, ciudad2):
    x1, y1 = ciudades[nombres_ciudades[ciudad1]]
    x2, y2 = ciudades[nombres_ciudades[ciudad2]]

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# ==================================================
# EVALUAR UNA RUTA
# ==================================================

def evaluar_ruta(individuo):
    distancia_total = 0

    for i in range(len(individuo)):
        ciudad_actual = individuo[i]
        ciudad_siguiente = individuo[(i + 1) % len(individuo)]

        distancia_total += distancia(ciudad_actual, ciudad_siguiente)

    # DEAP minimizara este valor.
    return (distancia_total,)


# ==================================================
# CONFIGURACION DE DEAP
# ==================================================

# Crear las clases solamente si no existen.
if not hasattr(creator, "FitnessMinTSP"):
    creator.create(
        "FitnessMinTSP",
        base.Fitness,
        weights=(-1.0,)
    )

if not hasattr(creator, "IndividualTSP"):
    creator.create(
        "IndividualTSP",
        list,
        fitness=creator.FitnessMinTSP
    )

toolbox = base.Toolbox()

# Cada individuo es una permutacion de las ciudades.
toolbox.register(
    "indices",
    random.sample,
    range(numero_ciudades),
    numero_ciudades
)

toolbox.register(
    "individual",
    tools.initIterate,
    creator.IndividualTSP,
    toolbox.indices
)

toolbox.register(
    "population",
    tools.initRepeat,
    list,
    toolbox.individual
)

toolbox.register("evaluate", evaluar_ruta)

# Seleccion por torneo.
toolbox.register("select", tools.selTournament, tournsize=3)

# Cruce apropiado para rutas representadas como permutaciones.
toolbox.register("mate", tools.cxOrdered)

# Mutacion por intercambio de posiciones.
toolbox.register(
    "mutate",
    tools.mutShuffleIndexes,
    indpb=0.15
)


# ==================================================
# PARAMETROS DEL ALGORITMO GENETICO
# ==================================================

TAMANO_POBLACION = 100
GENERACIONES = 30
PROBABILIDAD_CRUCE = 0.8
PROBABILIDAD_MUTACION = 0.2


# ==================================================
# EJECUTAR EL ALGORITMO GENETICO
# ==================================================

def ejecutar_algoritmo():
    poblacion = toolbox.population(n=TAMANO_POBLACION)

    # Registrar la mejor solucion inicial.
    distancias_iniciales = [
        toolbox.evaluate(individuo)[0]
        for individuo in poblacion
    ]

    mejor_inicial = min(distancias_iniciales)

    # Registrar estadisticas.
    estadisticas = tools.Statistics(
        lambda individuo: individuo.fitness.values[0]
    )

    estadisticas.register("min", min)
    estadisticas.register("avg", lambda valores: sum(valores) / len(valores))

    # Conservar la mejor solucion encontrada.
    archivo = tools.HallOfFame(1)

    # Ejecutar 30 generaciones.
    poblacion, historial = algorithms.eaSimple(
        poblacion,
        toolbox,
        cxpb=PROBABILIDAD_CRUCE,
        mutpb=PROBABILIDAD_MUTACION,
        ngen=GENERACIONES,
        stats=estadisticas,
        halloffame=archivo,
        verbose=False
    )

    mejor_individuo = archivo[0]
    mejor_distancia = evaluar_ruta(mejor_individuo)[0]

    return mejor_inicial, mejor_individuo, mejor_distancia, historial


# ==================================================
# MOSTRAR Y GUARDAR RESULTADOS
# ==================================================

def main():
    print("=" * 55)
    print("ACTIVIDAD 6: ALGORITMO GENETICO CON DEAP")
    print("Problema del viajante (TSP)")
    print("=" * 55)

    print("\nNumero de ciudades:", numero_ciudades)
    print("Tamano de la poblacion:", TAMANO_POBLACION)
    print("Numero de generaciones:", GENERACIONES)

    mejor_inicial, mejor_ruta, mejor_distancia, historial = (
        ejecutar_algoritmo()
    )

    ruta_nombres = [
        nombres_ciudades[indice]
        for indice in mejor_ruta
    ]

    ruta_cerrada = ruta_nombres + [ruta_nombres[0]]

    # Obtener la mejor distancia de cada generacion.
    mejores_generaciones = historial.select("min")
    promedios_generaciones = historial.select("avg")

    # La primera entrada del historial corresponde a la poblacion inicial.
    mejor_final_generacion = mejores_generaciones[-1]

    print("\n--- RESULTADOS ---")
    print("Mejor distancia inicial de la poblacion:",
          round(mejor_inicial, 2))

    print("Mejor ruta encontrada:")
    print(" -> ".join(ruta_cerrada))

    print("Distancia de la mejor ruta:",
          round(mejor_distancia, 2))

    print("Mejor distancia de la ultima generacion:",
          round(mejor_final_generacion, 2))

    print("\n--- RESUMEN DE CONVERGENCIA ---")
    print("Generaciones ejecutadas:", GENERACIONES)
    print("Mejor distancia registrada en la generacion inicial:",
          round(mejores_generaciones[0], 2))
    print("Mejor distancia registrada en la generacion final:",
          round(mejores_generaciones[-1], 2))

    # Guardar los resultados en un archivo de texto.
    with open("resultados_actividad6.txt", "w", encoding="utf-8") as archivo:
        archivo.write("ACTIVIDAD 6: ALGORITMO GENETICO CON DEAP\n")
        archivo.write("Problema del viajante (TSP)\n\n")
        archivo.write(f"Numero de ciudades: {numero_ciudades}\n")
        archivo.write(f"Tamano de poblacion: {TAMANO_POBLACION}\n")
        archivo.write(f"Generaciones: {GENERACIONES}\n")
        archivo.write(
            f"Mejor distancia inicial: {mejor_inicial:.2f}\n"
        )
        archivo.write("Mejor ruta encontrada:\n")
        archivo.write(" -> ".join(ruta_cerrada) + "\n")
        archivo.write(
            f"Distancia de la mejor ruta: {mejor_distancia:.2f}\n"
        )
        archivo.write(
            f"Mejor distancia final de la poblacion: "
            f"{mejor_final_generacion:.2f}\n"
        )

    # ==================================================
    # GRAFICA 1: RUTA ENCONTRADA
    # ==================================================

    plt.figure(figsize=(9, 7))

    x_ruta = [ciudades[nombre][0] for nombre in ruta_cerrada]
    y_ruta = [ciudades[nombre][1] for nombre in ruta_cerrada]

    plt.plot(
        x_ruta,
        y_ruta,
        marker="o",
        linewidth=2
    )

    for nombre, (x, y) in ciudades.items():
        plt.annotate(
            nombre,
            (x, y),
            xytext=(5, 5),
            textcoords="offset points"
        )

    plt.title("Mejor ruta encontrada por el algoritmo genetico")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("ruta_optima_actividad6.png", dpi=200)
    plt.show()

    # ==================================================
    # GRAFICA 2: CONVERGENCIA
    # ==================================================

    generaciones = list(range(len(mejores_generaciones)))

    plt.figure(figsize=(10, 6))

    plt.plot(
        generaciones,
        mejores_generaciones,
        marker="o",
        label="Mejor distancia"
    )

    plt.plot(
        generaciones,
        promedios_generaciones,
        linestyle="--",
        label="Distancia promedio"
    )

    plt.title("Convergencia del algoritmo genetico")
    plt.xlabel("Generacion")
    plt.ylabel("Distancia total")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("convergencia_actividad6.png", dpi=200)
    plt.show()

    print("\nArchivos generados:")
    print("1. ruta_optima_actividad6.png")
    print("2. convergencia_actividad6.png")
    print("3. resultados_actividad6.txt")
    print("\nPrograma finalizado correctamente.")


if __name__ == "__main__":
    main()
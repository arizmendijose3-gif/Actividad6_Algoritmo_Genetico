
import heapq
import time
import math
import matplotlib.pyplot as plt

# =====================================================
# ACTIVIDAD 5: BUSQUEDA CON HEURISTICAS A* Y DIJKSTRA
# =====================================================

# Cada ubicacion tiene coordenadas para dibujar la red.
# Las conexiones tienen costos expresados en kilometros.

ubicaciones = {
    "Inicio": (0, 0),
    "A": (2, 4),
    "B": (3, -2),
    "C": (5, 5),
    "D": (6, 1),
    "E": (7, -3),
    "Meta": (10, 1)
}

# Grafo no dirigido: cada conexion puede recorrerse
# en ambos sentidos y tiene un costo asociado.

grafo = {
    "Inicio": {"A": 4.5, "B": 3.8},
    "A": {"Inicio": 4.5, "C": 3.5, "D": 5.0},
    "B": {"Inicio": 3.8, "D": 4.0, "E": 4.2},
    "C": {"A": 3.5, "D": 3.0, "Meta": 6.0},
    "D": {"A": 5.0, "B": 4.0, "C": 3.0, "E": 3.5, "Meta": 4.5},
    "E": {"B": 4.2, "D": 3.5, "Meta": 4.0},
    "Meta": {"C": 6.0, "D": 4.5, "E": 4.0}
}

inicio = "Inicio"
objetivo = "Meta"


# =====================================================
# HEURISTICA
# =====================================================

def heuristica(nodo, destino):
    """
    Calcula una estimacion de la distancia en linea recta.
    Se utiliza para orientar la busqueda de A*.
    """
    x1, y1 = ubicaciones[nodo]
    x2, y2 = ubicaciones[destino]

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# =====================================================
# ALGORITMO DE DIJKSTRA
# =====================================================

def dijkstra(grafo, inicio, objetivo):
    cola = [(0, inicio)]
    costos = {nodo: float("inf") for nodo in grafo}
    anteriores = {}
    costos[inicio] = 0

    visitados = set()
    orden_explorado = []
    iteraciones = 0

    tiempo_inicio = time.perf_counter()

    while cola:
        costo_actual, nodo = heapq.heappop(cola)

        if nodo in visitados:
            continue

        visitados.add(nodo)
        orden_explorado.append(nodo)
        iteraciones += 1

        if nodo == objetivo:
            break

        for vecino, peso in grafo[nodo].items():
            nuevo_costo = costo_actual + peso

            if nuevo_costo < costos[vecino]:
                costos[vecino] = nuevo_costo
                anteriores[vecino] = nodo
                heapq.heappush(cola, (nuevo_costo, vecino))

    tiempo = time.perf_counter() - tiempo_inicio

    if costos[objetivo] == float("inf"):
        return None, float("inf"), orden_explorado, iteraciones, tiempo

    camino = reconstruir_camino(anteriores, inicio, objetivo)

    return camino, costos[objetivo], orden_explorado, iteraciones, tiempo


# =====================================================
# ALGORITMO A*
# =====================================================

def a_estrella(grafo, inicio, objetivo):
    cola = [(heuristica(inicio, objetivo), 0, inicio)]
    costos = {nodo: float("inf") for nodo in grafo}
    anteriores = {}

    costos[inicio] = 0

    visitados = set()
    orden_explorado = []
    iteraciones = 0

    tiempo_inicio = time.perf_counter()

    while cola:
        f_actual, g_actual, nodo = heapq.heappop(cola)

        if nodo in visitados:
            continue

        visitados.add(nodo)
        orden_explorado.append(nodo)
        iteraciones += 1

        if nodo == objetivo:
            break

        for vecino, peso in grafo[nodo].items():
            nuevo_costo = g_actual + peso

            if nuevo_costo < costos[vecino]:
                costos[vecino] = nuevo_costo
                anteriores[vecino] = nodo

                f_nuevo = nuevo_costo + heuristica(vecino, objetivo)

                heapq.heappush(
                    cola,
                    (f_nuevo, nuevo_costo, vecino)
                )

    tiempo = time.perf_counter() - tiempo_inicio

    if costos[objetivo] == float("inf"):
        return None, float("inf"), orden_explorado, iteraciones, tiempo

    camino = reconstruir_camino(anteriores, inicio, objetivo)

    return camino, costos[objetivo], orden_explorado, iteraciones, tiempo


# =====================================================
# RECONSTRUIR LA RUTA ENCONTRADA
# =====================================================

def reconstruir_camino(anteriores, inicio, objetivo):
    camino = [objetivo]
    actual = objetivo

    while actual != inicio:
        actual = anteriores[actual]
        camino.append(actual)

    camino.reverse()
    return camino


# =====================================================
# COMPROBAR ADMISIBILIDAD DE LA HEURISTICA
# =====================================================

def comprobar_heuristica():
    """
    Compara la estimacion heuristica con el costo minimo
    real hasta la meta, calculado mediante Dijkstra.
    """

    resultados = []

    for nodo in grafo:
        if nodo == objetivo:
            continue

        _, costo_real, _, _, _ = dijkstra(grafo, nodo, objetivo)
        estimacion = heuristica(nodo, objetivo)

        admisible = estimacion <= costo_real + 1e-9

        resultados.append(
            (nodo, estimacion, costo_real, admisible)
        )

    return resultados


# =====================================================
# DIBUJAR LA RED Y LAS RUTAS
# =====================================================

def dibujar_red(camino_a, camino_d):
    plt.figure(figsize=(10, 7))

    # Dibujar conexiones
    conexiones_dibujadas = set()

    for nodo, vecinos in grafo.items():
        x1, y1 = ubicaciones[nodo]

        for vecino, peso in vecinos.items():
            conexion = tuple(sorted((nodo, vecino)))

            if conexion in conexiones_dibujadas:
                continue

            conexiones_dibujadas.add(conexion)

            x2, y2 = ubicaciones[vecino]

            plt.plot(
                [x1, x2],
                [y1, y2],
                color="gray",
                linewidth=1.5,
                zorder=1
            )

            medio_x = (x1 + x2) / 2
            medio_y = (y1 + y2) / 2

            plt.text(
                medio_x,
                medio_y,
                str(peso),
                fontsize=8,
                bbox=dict(facecolor="white", alpha=0.8)
            )

    # Dibujar la ruta de Dijkstra
    if camino_d:
        for i in range(len(camino_d) - 1):
            n1 = camino_d[i]
            n2 = camino_d[i + 1]

            x1, y1 = ubicaciones[n1]
            x2, y2 = ubicaciones[n2]

            plt.plot(
                [x1, x2],
                [y1, y2],
                color="blue",
                linewidth=3,
                linestyle="--",
                label="Ruta Dijkstra" if i == 0 else "",
                zorder=2
            )

    # Dibujar la ruta de A*
    if camino_a:
        for i in range(len(camino_a) - 1):
            n1 = camino_a[i]
            n2 = camino_a[i + 1]

            x1, y1 = ubicaciones[n1]
            x2, y2 = ubicaciones[n2]

            plt.plot(
                [x1, x2],
                [y1, y2],
                color="red",
                linewidth=2,
                label="Ruta A*" if i == 0 else "",
                zorder=3
            )

    # Dibujar nodos
    for nodo, (x, y) in ubicaciones.items():
        plt.scatter(x, y, s=500, zorder=4)
        plt.text(
            x,
            y,
            nodo,
            ha="center",
            va="center",
            fontsize=9,
            color="white",
            fontweight="bold",
            zorder=5
        )

    plt.title("Red de transporte: comparacion A* y Dijkstra")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("red_transporte.png", dpi=200)
    plt.show()


# =====================================================
# DASHBOARD DE METRICAS
# =====================================================

def crear_dashboard(resultado_a, resultado_d):
    nombres = ["A*", "Dijkstra"]

    costos = [
        resultado_a[1],
        resultado_d[1]
    ]

    nodos_explorados = [
        len(resultado_a[2]),
        len(resultado_d[2])
    ]

    tiempos = [
        resultado_a[4] * 1000,
        resultado_d[4] * 1000
    ]

    fig, ejes = plt.subplots(1, 3, figsize=(14, 5))

    ejes[0].bar(nombres, costos)
    ejes[0].set_title("Costo total de la ruta")
    ejes[0].set_ylabel("Costo (km)")

    ejes[1].bar(nombres, nodos_explorados)
    ejes[1].set_title("Nodos explorados")
    ejes[1].set_ylabel("Cantidad")

    ejes[2].bar(nombres, tiempos)
    ejes[2].set_title("Tiempo de ejecucion")
    ejes[2].set_ylabel("Milisegundos")

    fig.suptitle("Dashboard comparativo de A* y Dijkstra")
    plt.tight_layout()
    plt.savefig("dashboard_comparativo.png", dpi=200)
    plt.show()


# =====================================================
# PROGRAMA PRINCIPAL
# =====================================================

if __name__ == "__main__":
    print("=" * 55)
    print("ACTIVIDAD 5: A* Y DIJKSTRA")
    print("=" * 55)

    print("\nPunto de inicio:", inicio)
    print("Destino:", objetivo)

    resultado_a = a_estrella(grafo, inicio, objetivo)
    resultado_d = dijkstra(grafo, inicio, objetivo)

    print("\n--- RESULTADOS DE A* ---")
    print("Ruta:", " -> ".join(resultado_a[0]))
    print("Costo total:", round(resultado_a[1], 2), "km")
    print("Nodos explorados:", resultado_a[2])
    print("Cantidad de nodos explorados:", len(resultado_a[2]))
    print("Iteraciones:", resultado_a[3])
    print("Tiempo:", round(resultado_a[4] * 1000, 4), "ms")

    print("\n--- RESULTADOS DE DIJKSTRA ---")
    print("Ruta:", " -> ".join(resultado_d[0]))
    print("Costo total:", round(resultado_d[1], 2), "km")
    print("Nodos explorados:", resultado_d[2])
    print("Cantidad de nodos explorados:", len(resultado_d[2]))
    print("Iteraciones:", resultado_d[3])
    print("Tiempo:", round(resultado_d[4] * 1000, 4), "ms")

    print("\n--- COMPROBACION DE LA HEURISTICA ---")

    resultados_heuristica = comprobar_heuristica()

    for nodo, estimacion, costo_real, admisible in resultados_heuristica:
        print(
            f"{nodo}: h(n)={estimacion:.2f}, "
            f"costo real={costo_real:.2f}, "
            f"admisible={admisible}"
        )

    heuristica_admisible = all(
        fila[3] for fila in resultados_heuristica
    )

    print("\n¿La heuristica es admisible?:", heuristica_admisible)

    print("\n--- COMPARACION FINAL ---")

    if abs(resultado_a[1] - resultado_d[1]) < 1e-9:
        print("Ambos algoritmos encontraron rutas con el mismo costo.")
    else:
        print("Los costos encontrados son diferentes. Revisar resultados.")

    print("\nSe generaran las graficas...")

    dibujar_red(resultado_a[0], resultado_d[0])
    crear_dashboard(resultado_a, resultado_d)

    print("\nArchivos generados:")
    print("1. red_transporte.png")
    print("2. dashboard_comparativo.png")
    print("\nPrograma finalizado correctamente.")


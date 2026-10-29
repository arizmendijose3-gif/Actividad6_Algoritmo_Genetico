from collections import deque

# Representacion del laberinto como un grafo.
# Cada lugar tiene conexiones con otros lugares.

grafo = {
    "Inicio": ["A", "B"],
    "A": ["Inicio", "C", "D"],
    "B": ["Inicio", "E"],
    "C": ["A", "Meta"],
    "D": ["A", "E"],
    "E": ["B", "D", "Meta"],
    "Meta": ["C", "E"]
}


def busqueda_bfs(grafo, inicio, objetivo):
    """
    BFS explora primero los nodos mas cercanos.
    En un grafo sin pesos encuentra el camino mas corto.
    """
    cola = deque([(inicio, [inicio])])
    visitados = set()
    orden_visita = []

    while cola:
        nodo, camino = cola.popleft()

        if nodo in visitados:
            continue

        visitados.add(nodo)
        orden_visita.append(nodo)

        if nodo == objetivo:
            return camino, orden_visita

        for vecino in grafo[nodo]:
            if vecino not in visitados:
                cola.append((vecino, camino + [vecino]))

    return None, orden_visita


def busqueda_dfs(grafo, inicio, objetivo):
    """
    DFS explora un camino en profundidad antes de regresar.
    No garantiza encontrar el camino mas corto.
    """
    pila = [(inicio, [inicio])]
    visitados = set()
    orden_visita = []

    while pila:
        nodo, camino = pila.pop()

        if nodo in visitados:
            continue

        visitados.add(nodo)
        orden_visita.append(nodo)

        if nodo == objetivo:
            return camino, orden_visita

        # Se agregan los vecinos a la pila.
        # El orden puede influir en el camino encontrado.
        for vecino in reversed(grafo[nodo]):
            if vecino not in visitados:
                pila.append((vecino, camino + [vecino]))

    return None, orden_visita


# Definimos el punto inicial y el destino.
inicio = "Inicio"
objetivo = "Meta"

# Ejecutamos ambos algoritmos.
camino_bfs, visitas_bfs = busqueda_bfs(grafo, inicio, objetivo)
camino_dfs, visitas_dfs = busqueda_dfs(grafo, inicio, objetivo)

# Mostramos los resultados.
print("===== RESULTADOS DE LA ACTIVIDAD 4 =====")

print("\nBUSQUEDA BFS")
print("Camino encontrado:", " -> ".join(camino_bfs))
print("Longitud del camino:", len(camino_bfs) - 1, "aristas")
print("Nodos visitados:", visitas_bfs)
print("Cantidad de nodos visitados:", len(visitas_bfs))

print("\nBUSQUEDA DFS")
print("Camino encontrado:", " -> ".join(camino_dfs))
print("Longitud del camino:", len(camino_dfs) - 1, "aristas")
print("Nodos visitados:", visitas_dfs)
print("Cantidad de nodos visitados:", len(visitas_dfs))

# Comparacion final.
print("\n===== COMPARACION =====")

if len(camino_bfs) <= len(camino_dfs):
    print("BFS encontro un camino igual o mas corto que DFS.")
else:
    print("DFS encontro un camino mas corto en este ejemplo.")

print("BFS es conveniente cuando se necesita el camino mas corto")
print("en un grafo sin pesos.")
print("DFS es util para explorar rutas y recorrer estructuras.")


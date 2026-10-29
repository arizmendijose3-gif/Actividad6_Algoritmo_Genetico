# ============================================================
# ACTIVIDAD 2: PROBLEMAS Y ESPACIOS DE BUSQUEDA
# Asignatura: Fundamentos de Inteligencia Artificial
# Universidad Politecnica de Atlautla
#
# Este programa modela dos problemas mediante grafos dirigidos
# y ponderados. Genera estados alcanzables, calcula rutas de
# menor costo y guarda diagramas de los resultados.
# ============================================================

import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


# ------------------------------------------------------------
# FUNCION 1: GENERAR LOS ESTADOS ALCANZABLES
# Utiliza un recorrido BFS para visitar los nodos alcanzables.
# ------------------------------------------------------------

def generar_estados(grafo, estado_inicial):

    # Comprobar que el estado inicial exista en el grafo
    if estado_inicial not in grafo:
        raise ValueError("El estado inicial no existe en el grafo.")

    # Cola para controlar el orden de exploracion
    cola = deque([estado_inicial])

    # Conjunto para evitar visitar dos veces el mismo estado
    visitados = {estado_inicial}

    # Lista que guardara el orden de los estados visitados
    estados = []

    # Recorrer los estados alcanzables
    while cola:

        actual = cola.popleft()
        estados.append(actual)

        # Revisar las conexiones que salen del estado actual
        for vecino in grafo.successors(actual):

            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)

    return estados


# ------------------------------------------------------------
# FUNCION 2: CALCULAR Y MOSTRAR LA RUTA DE MENOR COSTO
# Utiliza el algoritmo de Dijkstra mediante NetworkX.
# ------------------------------------------------------------

def resolver_problema(grafo, inicio, meta, nombre_problema):

    print("\n" + "=" * 55)
    print(nombre_problema.upper())
    print("=" * 55)

    # Generar los estados alcanzables desde el inicio
    estados = generar_estados(grafo, inicio)

    print("Estado inicial:", inicio)
    print("Estado objetivo:", meta)
    print("Estados alcanzables:", estados)

    # Comprobar si la meta puede alcanzarse
    if meta not in estados:
        print("No existe una ruta desde el inicio hasta la meta.")
        return None

    # Calcular la ruta de menor costo usando los pesos
    ruta = nx.shortest_path(
        grafo,
        source=inicio,
        target=meta,
        weight="weight",
        method="dijkstra"
    )

    # Calcular el costo total de la ruta
    costo_total = nx.shortest_path_length(
        grafo,
        source=inicio,
        target=meta,
        weight="weight",
        method="dijkstra"
    )

    print("Ruta de menor costo:", " -> ".join(ruta))
    print("Costo total:", costo_total)

    # Devolver la ruta y el costo para usarlos en el dibujo
    return ruta, costo_total


# ------------------------------------------------------------
# FUNCION 3: DIBUJAR EL GRAFO Y RESALTAR LA RUTA ENCONTRADA
# Guarda el resultado en un archivo PNG.
# ------------------------------------------------------------

def dibujar_grafo(grafo, ruta, titulo, nombre_archivo):

    # Crear una distribucion visual de los nodos
    posicion = nx.spring_layout(grafo, seed=42)

    # Crear la figura
    plt.figure(figsize=(11, 7))

    # Dibujar todos los nodos y conexiones
    nx.draw_networkx_nodes(
        grafo,
        posicion,
        node_size=2200
    )

    nx.draw_networkx_labels(
        grafo,
        posicion,
        font_size=9
    )

    nx.draw_networkx_edges(
        grafo,
        posicion,
        arrows=True,
        arrowsize=20,
        connectionstyle="arc3,rad=0.05"
    )

    # Obtener los costos de las conexiones
    etiquetas = nx.get_edge_attributes(grafo, "weight")

    # Mostrar los costos en el diagrama
    nx.draw_networkx_edge_labels(
        grafo,
        posicion,
        edge_labels=etiquetas,
        font_size=9
    )

    # Si se encontro una ruta, resaltarla
    if ruta is not None:

        conexiones_ruta = list(zip(ruta[:-1], ruta[1:]))

        nx.draw_networkx_edges(
            grafo,
            posicion,
            edgelist=conexiones_ruta,
            edge_color="red",
            width=3,
            arrows=True,
            arrowsize=25,
            connectionstyle="arc3,rad=0.05"
        )

    # Agregar el titulo
    plt.title(titulo, fontsize=14)

    # Ajustar los espacios de la imagen
    plt.axis("off")
    plt.tight_layout()

    # Guardar la imagen en la carpeta del proyecto
    plt.savefig(
        nombre_archivo,
        dpi=200,
        bbox_inches="tight"
    )

    print("Diagrama guardado:", nombre_archivo)

    # Mostrar la imagen en pantalla
    plt.show()

    # Cerrar la figura para liberar recursos
    plt.close()


# ============================================================
# PROBLEMA 1: RUTA DESDE UNA CASA HASTA UN HOSPITAL
# ============================================================

# Crear un grafo dirigido
transporte = nx.DiGraph()

# Agregar conexiones y costos hipoteticos
transporte.add_weighted_edges_from([
    ("Casa", "Avenida", 4),
    ("Casa", "Parque", 2),
    ("Avenida", "Hospital", 7),
    ("Parque", "Hospital", 6),
    ("Parque", "Mercado", 3),
    ("Mercado", "Hospital", 2),
    ("Avenida", "Mercado", 2)
])

# Definir el inicio y el destino
inicio_transporte = "Casa"
meta_transporte = "Hospital"

# Resolver el primer problema
resultado_transporte = resolver_problema(
    transporte,
    inicio_transporte,
    meta_transporte,
    "Problema 1: Ruta de una casa a un hospital"
)

# Obtener la ruta para dibujarla
if resultado_transporte is not None:

    ruta_transporte, costo_transporte = resultado_transporte

else:

    ruta_transporte = None

# Generar el diagrama del primer problema
dibujar_grafo(
    transporte,
    ruta_transporte,
    "Problema 1: Ruta de menor costo al hospital",
    "grafo_transporte.png"
)


# ============================================================
# PROBLEMA 2: RUTA DENTRO DE UN ALMACEN
# ============================================================

# Crear un grafo dirigido
almacen = nx.DiGraph()

# Agregar conexiones y costos hipoteticos
almacen.add_weighted_edges_from([
    ("Entrada", "Pasillo_A", 2),
    ("Entrada", "Pasillo_B", 4),
    ("Pasillo_A", "Zona_Almacen", 3),
    ("Pasillo_A", "Zona_Empaque", 5),
    ("Pasillo_B", "Zona_Empaque", 2),
    ("Zona_Almacen", "Zona_Empaque", 2),
    ("Zona_Empaque", "Salida", 3),
    ("Pasillo_B", "Salida", 8)
])

# Definir el inicio y el destino
inicio_almacen = "Entrada"
meta_almacen = "Salida"

# Resolver el segundo problema
resultado_almacen = resolver_problema(
    almacen,
    inicio_almacen,
    meta_almacen,
    "Problema 2: Ruta dentro de un almacen"
)

# Obtener la ruta para dibujarla
if resultado_almacen is not None:

    ruta_almacen, costo_almacen = resultado_almacen

else:

    ruta_almacen = None

# Generar el diagrama del segundo problema
dibujar_grafo(
    almacen,
    ruta_almacen,
    "Problema 2: Ruta de menor costo en el almacen",
    "grafo_almacen.png"
)


# ============================================================
# FIN DEL PROGRAMA
# ============================================================

print("\nEjecucion finalizada.")
print("Revisa las imagenes PNG generadas en la carpeta del proyecto.")
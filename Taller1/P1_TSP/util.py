import random
import string
import math
import time
import networkx as nx

from collections import deque
from matplotlib import pyplot as plt

def generar_ciudades(n_cities: int, seed: int = 123):
    random.seed(seed)  # This fixes the seed for reproducibility
    cities = {}
    for i in range(n_cities):
        ciudad = f"{random.choice(string.ascii_uppercase)}{random.randint(0,9)}"
        x = round(random.uniform(-100, 100) ,1) # Coordenada x aleatoria entre -100 y 100
        y = round(random.uniform(-100, 100), 1)  # Coordenada y aleatoria entre -100 y 100
        cities[ciudad] = (x, y)
    return cities

def calcular_distancia(ciudad1, ciudad2):
    x1, y1 = ciudad1
    x2, y2 = ciudad2
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia

def generar_distancias(ciudades):
    distancias = {}
    for ciudad1, coord1 in ciudades.items():
        for ciudad2, coord2 in ciudades.items():
            if ciudad1 != ciudad2:
                distancia = calcular_distancia(coord1, coord2)
                distancias[(ciudad1, ciudad2)] = distancia
    return distancias

def generar_ciudades_con_distancias(n_cities: int):
    ciudades = generar_ciudades(n_cities)
    distancias = generar_distancias(ciudades)
    return ciudades, distancias

def plotear_ruta(ciudades, ruta, mostrar_anotaciones=True):
    # Extraer coordenadas de las ciudades
    coordenadas_x = [ciudades[ciudad][0] for ciudad in ruta]
    coordenadas_y = [ciudades[ciudad][1] for ciudad in ruta]

    # Agregar la primera ciudad al final para cerrar el ciclo
    coordenadas_x.append(coordenadas_x[0])
    coordenadas_y.append(coordenadas_y[0])

    print({coordenadas_x[0]} , {coordenadas_y[0]})

    # Trama de las ubicaciones de las ciudades
    plt.figure(figsize=(8, 6))
    plt.scatter(coordenadas_x, coordenadas_y, color='blue', label='Ciudades')

    # Trama del mejor camino encontrado
    plt.plot(coordenadas_x, coordenadas_y, linestyle='-', marker='o', color='red', label='Mejor Ruta')

    if mostrar_anotaciones:
        # Anotar las letras de las ciudades
        for i, ciudad in enumerate(ruta):
            plt.text(coordenadas_x[i], coordenadas_y[i], ciudad)

    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.title('Ubicaciones de las Ciudades y Mejor Ruta')
    plt.legend()
    plt.grid(True)
    plt.show()


def bfs(ciudades, distancias):
    mejor_ruta = None
    menor_distancia = math.inf

    G = nx.Graph()
    for (ciudad_origen, ciudad_destino), distancia in distancias.items():
        G.add_edge(ciudad_origen, ciudad_destino, weight=distancia)

    # Nodos y filos del grafo
    #print("Nodos del grafo:", G.nodes())
    #print("Filos del grafo con pesos:", G.edges(data=True))

    # Cola para BFS: cada elemento es una tupla (ruta_actual, distancia_actual)
    ciudades = list(ciudades.keys())
    cola = deque([([ciudad], 0) for ciudad in ciudades])

    # Medición de tiempo
    start_time = time.time()

    while cola:
        ruta_actual, distancia_actual = cola.popleft()

        # Si la ruta incluye todas las ciudades y regresa al origen, evaluar
        if len(ruta_actual) == len(ciudades):
            distancia_total = distancia_actual + G[ruta_actual[-1]][ruta_actual[0]]['weight']
            if distancia_total < menor_distancia:
                menor_distancia = distancia_total
                mejor_ruta = ruta_actual
            continue

        # Expandir la ruta actual con las ciudades restantes
        for ciudad in ciudades:
            if ciudad not in ruta_actual:
                nueva_ruta = ruta_actual + [ciudad]
                nueva_distancia = distancia_actual + G[ruta_actual[-1]][ciudad]['weight']
                cola.append((nueva_ruta, nueva_distancia))

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo para encontrar la ruta más corta entre {len(ciudades)} ciudades con BFS: {elapsed_time:.4f} segundos")

    return list(mejor_ruta)



def dfs(ciudades, distancias):
    mejor_ruta = None
    menor_distancia = math.inf

    G = nx.Graph()
    for (ciudad_origen, ciudad_destino), distancia in distancias.items():
        G.add_edge(ciudad_origen, ciudad_destino, weight=distancia)

    # Lista para DFS: cada elemento es una tupla (ruta_actual, distancia_actual)
    ciudades = list(ciudades.keys())
    stack = [([ciudad], 0) for ciudad in ciudades]

    # Medición de tiempo
    start_time = time.time()

    while stack:
        ruta_actual, distancia_actual = stack.pop()

        # Si la ruta incluye todas las ciudades y regresa al origen, evaluar
        if len(ruta_actual) == len(ciudades):
            distancia_total = distancia_actual + G[ruta_actual[-1]][ruta_actual[0]]['weight']
            if distancia_total < menor_distancia:
                menor_distancia = distancia_total
                mejor_ruta = ruta_actual
            continue

        # Expandir la ruta actual con las ciudades restantes
        for ciudad in ciudades:
            if ciudad not in ruta_actual:
                nueva_ruta = ruta_actual + [ciudad]
                nueva_distancia = distancia_actual + G[ruta_actual[-1]][ciudad]['weight']
                stack.append((nueva_ruta, nueva_distancia))
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo para encontrar la ruta más corta entre {len(ciudades)} ciudades con DFS: {elapsed_time:.4f} segundos")

    return list(mejor_ruta)




def a_star(ciudades, distancias):
    mejor_ruta = None
    menor_distancia = math.inf

    G = nx.Graph()
    for (ciudad_origen, ciudad_destino), distancia in distancias.items():
        G.add_edge(ciudad_origen, ciudad_destino, weight=distancia)

    # Lista de ciudades
    ciudades = list(ciudades.keys())

    # Función heurística: distancia mínima desde la ciudad actual a cualquier otra ciudad no visitada
    def heuristica(ciudad_actual, no_visitadas):
        if not no_visitadas:
            return 0
        return min(
            G[ciudad_actual][ciudad]['weight'] if ciudad in G[ciudad_actual] else math.inf
            for ciudad in no_visitadas
        )

    # Cola de prioridad para A*: cada elemento es una tupla (costo_estimado, ruta_actual, distancia_actual)
    from heapq import heappush, heappop
    cola = []
    for ciudad in ciudades:
        heappush(cola, (0, [ciudad], 0))  # Inicializar con cada ciudad como punto de partida

    # Medición de tiempo
    start_time = time.time()

    while cola:
        costo_estimado, ruta_actual, distancia_actual = heappop(cola)

        # Si la ruta incluye todas las ciudades y regresa al origen, evaluar
        if len(ruta_actual) == len(ciudades):
            if ruta_actual[-1] in G and ruta_actual[0] in G[ruta_actual[-1]]:
                distancia_total = distancia_actual + G[ruta_actual[-1]][ruta_actual[0]]['weight']
                if distancia_total < menor_distancia:
                    menor_distancia = distancia_total
                    mejor_ruta = ruta_actual
            continue

        # Expandir la ruta actual con las ciudades restantes
        no_visitadas = [ciudad for ciudad in ciudades if ciudad not in ruta_actual]
        for ciudad in no_visitadas:
            if ciudad in G[ruta_actual[-1]]:  # Verificar si hay un filo
                nueva_ruta = ruta_actual + [ciudad]
                nueva_distancia = distancia_actual + G[ruta_actual[-1]][ciudad]['weight']
                costo_heuristico = nueva_distancia + heuristica(ciudad, no_visitadas)
                heappush(cola, (costo_heuristico, nueva_ruta, nueva_distancia))
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo para encontrar la ruta más corta entre {len(ciudades)} ciudades con A*: {elapsed_time:.4f} segundos")

    return list(mejor_ruta)


def vecinos_cercanos(ciudades, distancias):
    mejor_ruta = []
    menor_distancia = 0

    G = nx.Graph()
    for (ciudad_origen, ciudad_destino), distancia in distancias.items():
        G.add_edge(ciudad_origen, ciudad_destino, weight=distancia)

    # Lista de ciudades
    ciudades = list(ciudades.keys())
    ciudad_actual = ciudades[0]  # Comenzar desde la primera ciudad
    mejor_ruta.append(ciudad_actual)

    # Medición de tiempo
    start_time = time.time()

    while len(mejor_ruta) < len(ciudades):
        # Encontrar la ciudad más cercana no visitada
        ciudad_mas_cercana = None
        distancia_mas_corta = math.inf
        for vecino in G[ciudad_actual]:
            if vecino not in mejor_ruta and G[ciudad_actual][vecino]['weight'] < distancia_mas_corta:
                ciudad_mas_cercana = vecino
                distancia_mas_corta = G[ciudad_actual][vecino]['weight']

        # Agregar la ciudad más cercana a la ruta
        mejor_ruta.append(ciudad_mas_cercana)
        menor_distancia += distancia_mas_corta
        ciudad_actual = ciudad_mas_cercana

    # Volver a la ciudad de origen
    menor_distancia += G[mejor_ruta[-1]][mejor_ruta[0]]['weight']
    mejor_ruta.append(mejor_ruta[0])

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo para encontrar la ruta más corta entre {len(ciudades)} ciudades con Vecinos Cercanos: {elapsed_time:.4f} segundos")

    return mejor_ruta
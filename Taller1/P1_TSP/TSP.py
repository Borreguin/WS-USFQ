import math
import networkx as nx
import matplotlib.pyplot as plt  # Asegúrate de importar matplotlib


from typing import List
from itertools import permutations
from collections import deque



#from Taller1.P1_TSP.util import plotear_ruta, generar_ciudades_con_distancias
from util import plotear_ruta, generar_ciudades_con_distancias, bfs, dfs, a_star



class TSP:
    def __init__(self, ciudades, distancias):
        self.ciudades = ciudades
        self.distancias = distancias

    def encontrar_la_ruta_mas_corta(self, algoritmo="bfs"):
        if algoritmo == "bfs":
            mejor_ruta = bfs(self.ciudades, self.distancias)
        elif algoritmo == "dfs":
            mejor_ruta = dfs(self.ciudades, self.distancias)
        elif algoritmo == "a_star":
            mejor_ruta = a_star(self.ciudades, self.distancias)
        else:
            raise ValueError("Algoritmo no soportado. Usa 'bfs', 'dfs' o 'a_star'.")
        return mejor_ruta


    def plotear_resultado(self, ruta: List[str], mostrar_anotaciones: bool = True):
        plotear_ruta(self.ciudades, ruta, mostrar_anotaciones)


def study_case_1(algoritmo="bfs"):
    n_cities = 10 # En 12 se cuelga
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias)

    rutas = []
    rutas.append(ciudades.keys())
    rutas.append(tsp.encontrar_la_ruta_mas_corta(algoritmo))
    
    for ruta in rutas:
        tsp.plotear_resultado(ruta)


def study_case_2():
    n_cities = 100
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias)
    
    ruta = ciudades.keys()
    ruta = tsp.encontrar_la_ruta_mas_corta()
    
    tsp.plotear_resultado(ruta)

def menu():
    print("El programa mostrara primero las ciudades generadas y luego la ruta más corta encontrada\n")
    print("Seleccione el algoritmo para resolver el TSP:")
    print("1. BFS")
    print("2. DFS")
    print("3. A*")
    opcion = input("Ingrese el número de la opción deseada: ")

    if opcion == "1":
        algoritmo = "bfs"
    elif opcion == "2":
        algoritmo = "dfs"
    elif opcion == "3":
        algoritmo = "a_star"
    else:
        print("Opción no válida. Usando BFS por defecto.")
        algoritmo = "bfs"
    
    return algoritmo


if __name__ == "__main__":
    algoritmo = menu()

    # Solve the TSP problem
    study_case_1(algoritmo)
    #study_case_2()
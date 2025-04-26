from typing import List
import pandas as pd
import time
from Taller1.P1_TSP.util import plotear_ruta, generar_ciudades_con_distancias
from itertools import permutations

class TSP:
    @staticmethod
    def medir_tiempo(func):
        def envoltura(*args, **kwargs):
            inicio = time.time()  # Registro del tiempo inicial
            resultado = func(*args, **kwargs)  # Ejecución de la función
            fin = time.time()  # Registro del tiempo final
            print(f"Tiempo de ejecución de '{func.__name__}': {fin - inicio:.5f} segundos")
            return resultado  # Retorno del resultado de la función original

        return envoltura

    def __init__(self, ciudades, distancias):
        self.ciudades = ciudades
        self.distancias = distancias

    def encontrar_la_ruta_mas_corta(self):
        # Numero de ciudades
        num_ciudades = len(self.ciudades)

        # Definir umbrales de num_ciudades para seleccionar un algoritmo
        if num_ciudades <= 10:
            # Fuerza bruta
            print('Usando Fuerza Bruta')
            ruta_optima, distancia_minima = self._fuerza_bruta()
        elif num_ciudades <= 50:
            # Usar el vecino más cercano para entre 11 y 50 ciudades
            print("Usando Algoritmo del Vecino Más Cercano")
            ruta_optima, distancia_minima = self._vecino_mas_cercano()
        else:
            # Usar heurística para más de 50 ciudades
            print("Usando Algoritmo Heurístico")
            ruta_optima, distancia_minima = self._heuristica()

        print(f"Ruta óptima: {ruta_optima}")
        print(f"Distancia mínima: {distancia_minima}")
        return ruta_optima

    @medir_tiempo
    def _fuerza_bruta(self):
        ciudades = list(self.ciudades.keys())
        mejor_ruta = None
        distancia_minima = float('inf')

        # Permutaciones de las ciudades
        #print(self.distancias)
        for perm in permutations(ciudades):
            distancia_total = self._calcular_distancia_total(perm)

            # Actualizar la mejor ruta
            if distancia_total < distancia_minima:
                distancia_minima = distancia_total
                mejor_ruta = perm

        return list(mejor_ruta), distancia_minima

    @medir_tiempo
    def _vecino_mas_cercano(self):
        ciudades = list(self.ciudades.keys())
        ciudad_actual = ciudades[0]
        ruta = [ciudad_actual]
        distancia_total = 0

        while len(ruta) < len(ciudades):
            # Encontrar la ciudad más cercana no visitada
            ciudad_mas_cercana = min(
                (ciudad for ciudad in ciudades if ciudad not in ruta),
                key=lambda ciudad: self.distancias[(ciudad_actual,ciudad)]
            )
            distancia_total += self.distancias[(ciudad_actual, ciudad_mas_cercana)]
            ruta.append(ciudad_mas_cercana)
            ciudad_actual = ciudad_mas_cercana

        # Cierre del ciclo
        distancia_total += self.distancias[(ruta[-1],ruta[0])]
        return ruta, distancia_total

    @medir_tiempo
    def _heuristica(self):
        import random
        ciudades = list(self.ciudades.keys())
        ruta = random.sample(ciudades, len(ciudades))  # Solución inicial aleatoria
        distancia_total = self._calcular_distancia_total(ruta)  # Método para calcular la distancia total de una ruta
        return ruta, distancia_total

    def _calcular_distancia_total(self, ruta):
        distancia_total = 0
        for i in range(len(ruta) - 1):
            distancia_total += self.distancias[(ruta[i], ruta[i + 1])]
        distancia_total += self.distancias[(ruta[-1], ruta[0])]  # Cierre del ciclo
        return distancia_total

    def plotear_resultado(self, ruta: List[str], mostrar_anotaciones: bool = True):
        plotear_ruta(self.ciudades, ruta, mostrar_anotaciones)

    @staticmethod
    def matriz(ruta: List[str]):
        conexiones=ruta
        nodos = sorted(set(conexiones))

        matriz = pd.DataFrame(0,index=nodos,columns =nodos)

        for i in range(len(conexiones)-1):
            origen = conexiones[i]
            destino = conexiones[i+1]
            matriz.loc[origen,destino] = 1
            matriz.loc[destino,origen] = 1
        print('Matriz Adyacente')
        print(matriz)





def study_case_1(n_cities = 3):
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias)
    #ruta = ciudades.keys()
    ruta = tsp.encontrar_la_ruta_mas_corta()
    tsp.plotear_resultado(ruta)
    tsp.matriz(ruta)



if __name__ == "__main__":
    # Solve the TSP problem
    # Solucion para 8 ciudades
    study_case_1(3)
    # Solucion para 50 ciudades
    study_case_1(51)
    # Solucion para 100 ciudades
    study_case_1(100)
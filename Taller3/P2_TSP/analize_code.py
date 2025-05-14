# Import libraries
import pandas as pd
import numpy as np
from TSP import *


# Redefine case 1 function

def study_case(n_cities:int = 10, heuristics:list[str] = [], mipgap=.05, time_limit:int =30,
                 plot:bool = True):
	
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tee = False
    tsp = TSP(ciudades, distancias, heuristics)
    ruta, time = tsp.encontrar_la_ruta_mas_corta(mipgap, time_limit, tee)
    tsp.plotear_resultado(ruta)
    return time

def part_A():
    num_cities = [10, 20, 30, 40, 50]
    times = []
    for i in num_cities:
        times.append(study_case(n_cities=i, plot=True).total_seconds()*1000)

    plt.plot(num_cities, times)
    plt.xlabel('Number of Cities')
    plt.ylabel('Time (ms)')
    plt.show()    


def part_B():
    heuristics = [['limitar_funcion_objetivo'], []]
    for i in heuristics:
        _ = study_case(heuristics= i, n_cities=70, plot=True)


part = 'B'

if part == 'A':
    part_A()
elif part == 'B':
    part_B()
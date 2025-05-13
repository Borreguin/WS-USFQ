# Import libraries
import pandas as pd
import numpy as np
from TSP import *


# Redefine case 1 function

def study_case_1(n_cities:int = 10, heuristics:list[str] = [], mipgap=.05, time_limit:int =30,
                 plot:bool = True):
	
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tee = False
    tsp = TSP(ciudades, distancias, heuristics)
    ruta, time = tsp.encontrar_la_ruta_mas_corta(mipgap, time_limit, tee)
    tsp.plotear_resultado(ruta)
    return time

if __name__=='__main__':
    num_cities = [10, 20, 30, 40, 50]
    times = []
    for i in num_cities:
        times.append(study_case_1(n_cities=i, plot=True).total_seconds()*1000)

    plt.plot(num_cities, times)
    plt.xlabel('Number of Cities')
    plt.ylabel('Time (ms)')
    plt.show()    

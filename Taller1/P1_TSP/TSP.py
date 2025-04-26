from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from typing import List

from Taller1.P1_TSP.util import plotear_ruta, generar_ciudades_con_distancias


class TSP:
    def __init__(self, ciudades, distancias):
        self.ciudades = ciudades
        self.distancias = distancias

    def encontrar_la_ruta_mas_corta(self)-> List[str]:
        n = len(self.distancias)
        gestor = pywrapcp.RoutingIndexManager(n, 1, 0)
        modelo = pywrapcp.RoutingModel(gestor)
        
        def distancia_callback(i, j):
            return int(self.distancias[gestor.IndexToNode(i)][gestor.IndexToNode(j)])

        transit_callback_index = modelo.RegisterTransitCallback(distancia_callback)
        modelo.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        parametros = pywrapcp.DefaultRoutingSearchParameters()
        parametros.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )

        solucion = modelo.SolveWithParameters(parametros)

        if not solucion:
            print("No se encontró solución")
            return []
        indice = modelo.Start(0)
        ruta_indices = []
        while not modelo.IsEnd(indice):
            nodo = gestor.IndexToNode(indice)
            ruta_indices.append(nodo)
            indice = solucion.Value(modelo.NextVar(indice))
        ruta_indices.append(ruta_indices[0])


        #pass
        # implementación aquí

    def plotear_resultado(self, ruta: List[str], mostrar_anotaciones: bool = True):
        plotear_ruta(self.ciudades, ruta, mostrar_anotaciones)


def study_case_1():
    n_cities = 10
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias)
    ruta = ciudades.keys()
    # ruta = tsp.encontrar_la_ruta_mas_corta()
    tsp.plotear_resultado(ruta)

def study_case_2():
    n_cities = 100
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias)
    ruta = ciudades.keys()
    # ruta = tsp.encontrar_la_ruta_mas_corta()
    tsp.plotear_resultado(ruta, True)


if __name__ == "__main__":
    # Solve the TSP problem
    study_case_1()
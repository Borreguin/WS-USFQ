import math
from collections import defaultdict
import pyomo.environ as pyo
from typing import List, Dict, Tuple
import datetime as dt


class VRP:
    def __init__(self, ciudades, distancias, demands, heuristics: List[str]):
        self.ciudades = ciudades
        self.distancias = distancias
        self.demands = demands
        self.heuristics = heuristics
        self.min_distance = self.get_min_distance()
        self.max_distance = self.get_max_distance()
        self.average_distance = self.get_average_distance()
        self.cal_min_max_distances()

    def get_min_distance(self):
        return min(d for d in self.distancias.values() if d > 0)

    def get_max_distance(self):
        return max(self.distancias.values())

    def get_average_distance(self):
        total = sum(self.distancias.values())
        count = len(self.distancias) - len(self.ciudades)  # Excluir diagonales
        return total / count

    def cal_min_max_distances(self):
        medium_low_distance = (self.min_distance + self.average_distance) / 2
        self.min_possible_distance = medium_low_distance * \
            len(self.ciudades) * 0.25
        self.max_possible_distance = medium_low_distance * \
            len(self.ciudades) * 0.6

    def nearest_neighbor_heuristic(self, vehicle_capacity: int, num_vehicles: int = None):
        """Implementación de la heurística del vecino más cercano para VRP"""
        unvisited = set(self.ciudades.keys()) - \
            {0}  # Todos los nodos excepto el depósito
        routes = []
        current_vehicles = 0

        # Si no se especifica num_vehicles, calculamos el mínimo teórico
        if num_vehicles is None:
            total_demand = sum(self.demands.values())
            num_vehicles = math.ceil(total_demand / vehicle_capacity)

        while unvisited and current_vehicles < num_vehicles:
            current_load = 0
            current_location = 0  # Depósito
            route = [current_location]

            while unvisited and current_vehicles < num_vehicles:
                # Encontrar el vecino más cercano que no exceda la capacidad
                nearest = None
                min_dist = float('inf')

                for city in unvisited:
                    if self.demands[city] + current_load <= vehicle_capacity:
                        dist = self.distancias[current_location, city]
                        if dist < min_dist:
                            min_dist = dist
                            nearest = city

                if nearest is None:
                    break  # No hay más clientes que puedan ser atendidos

                route.append(nearest)
                unvisited.remove(nearest)
                current_load += self.demands[nearest]
                current_location = nearest

            # Volver al depósito
            route.append(0)
            routes.append(route)
            current_vehicles += 1

        # Si quedan nodos sin visitar, necesitamos más vehículos
        if unvisited:
            return None

        return routes

    def solve_vrp(self, vehicle_capacity=None, num_vehicles=None, mipgap=0.1, time_limit=300, tee=False):
        start_time = dt.datetime.now()

        # Primero intentar con la heurística si está activada
        if "vecino_cercano" in self.heuristics and vehicle_capacity is not None:
            nn_routes = self.nearest_neighbor_heuristic(
                vehicle_capacity, num_vehicles)
            if nn_routes:
                print(
                    "Solución inicial encontrada con heurística del vecino más cercano:")
                total_distance = self.calculate_routes_distance(nn_routes)
                print(f"Distancia total: {total_distance}")
                print("Rutas:")
                for i, route in enumerate(nn_routes):
                    print(f"Vehículo {i+1}: {route}")

                # Si solo queremos la solución heurística
                if "solo_heuristica" in self.heuristics:
                    return nn_routes, total_distance

        # Continuar con la solución exacta si es necesario
        model = pyo.ConcreteModel()
        cities = list(self.ciudades.keys())
        n_cities = len(cities)
        depot = 0

        # Sets
        model.M = pyo.Set(initialize=cities)
        model.N = pyo.Set(initialize=cities)
        model.K = pyo.Set(initialize=range(num_vehicles)
                          if num_vehicles else [0])

        # Variables
        model.x = pyo.Var(model.N, model.M, model.K, within=pyo.Binary)
        model.u = pyo.Var(model.N, bounds=(0, n_cities),
                          within=pyo.NonNegativeIntegers)

        # Objective Function
        def obj_rule(model):
            return sum(self.distancias[i, j] * model.x[i, j, k]
                       for i in model.N for j in model.M for k in model.K if i != j)
        model.obj = pyo.Objective(rule=obj_rule, sense=pyo.minimize)

        # Constraints
        # Cada cliente visitado exactamente una vez (excepto depósito)
        def visit_once_rule(model, j):
            if j == depot:
                return pyo.Constraint.Skip
            return sum(model.x[i, j, k] for i in model.N for k in model.K if i != j) == 1
        model.visit_once = pyo.Constraint(model.M, rule=visit_once_rule)

        # Flujo de entrada y salida balanceado
        def flow_balance_rule(model, i, k):
            if i == depot:
                return sum(model.x[i, j, k] for j in model.M if j != i) - sum(model.x[j, i, k] for j in model.N if j != i) <= 1
            else:
                return sum(model.x[i, j, k] for j in model.M if j != i) - sum(model.x[j, i, k] for j in model.N if j != i) == 0
        model.flow_balance = pyo.Constraint(
            model.N, model.K, rule=flow_balance_rule)

        # Restricción de capacidad
        if vehicle_capacity is not None:
            def capacity_rule(model, k):
                return sum(self.demands[i] * model.x[i, j, k] for i in model.N for j in model.M if i != j) <= vehicle_capacity
            model.capacity = pyo.Constraint(model.K, rule=capacity_rule)

        # Restricción para evitar subtours (MTZ)
        def subtour_elimination_rule(model, i, j, k):
            if i != j and i != depot and j != depot:
                return model.u[i] - model.u[j] + n_cities * model.x[i, j, k] <= n_cities - 1
            return pyo.Constraint.Skip
        model.subtour_elim = pyo.Constraint(
            model.N, model.M, model.K, rule=subtour_elimination_rule)

        # Inicialización con solución heurística si está disponible
        if "vecino_cercano" in self.heuristics and nn_routes:
            for k, route in enumerate(nn_routes):
                for i in range(len(route)-1):
                    model.x[route[i], route[i+1], k].value = 1

        # Resolver el modelo
        solver = pyo.SolverFactory('glpk')
        solver.options['mipgap'] = mipgap
        solver.options['tmlim'] = time_limit
        results = solver.solve(model, tee=tee)

        execution_time = dt.datetime.now() - start_time
        print(f"Tiempo de ejecución: {delta_time_mm_ss(execution_time)}")

        # Procesar resultados
        if results.solver.termination_condition == pyo.TerminationCondition.optimal:
            print("Solución óptima encontrada:")
            routes = self.extract_routes(
                model, num_vehicles if num_vehicles else 1)
            total_distance = self.calculate_routes_distance(routes)
            print(f"Distancia total recorrida: {total_distance}")
            return routes, total_distance
        else:
            print("No se encontró solución óptima")
            return None, None

    def extract_routes(self, model, num_vehicles):
        routes = defaultdict(list)
        for k in range(num_vehicles):
            current_city = 0  # Depósito
            route = [current_city]
            visited = set()
            while True:
                next_cities = [j for j in model.M
                               if pyo.value(model.x[current_city, j, k]) > 0.5 and j not in visited]
                # Regreso al depósito
                if not next_cities or next_cities[0] == 0:
                    break
                current_city = next_cities[0]
                route.append(current_city)
                visited.add(current_city)
            route.append(0)  # Volver al depósito
            routes[k] = route
        return routes

    def calculate_routes_distance(self, routes):
        total_distance = 0
        if isinstance(routes, dict):  # Resultado del modelo
            for k, route in routes.items():
                for i in range(len(route)-1):
                    total_distance += self.distancias[route[i], route[i+1]]
        elif isinstance(routes, list):  # Resultado de la heurística
            for route in routes:
                for i in range(len(route)-1):
                    total_distance += self.distancias[route[i], route[i+1]]
        return total_distance

    def find_min_vehicles(self, vehicle_capacity):
        total_demand = sum(self.demands.values())
        min_vehicles = math.ceil(total_demand / vehicle_capacity)

        # Primero intentar con la heurística
        if "vecino_cercano" in self.heuristics:
            for num_vehicles in range(min_vehicles, len(self.ciudades)):
                routes = self.nearest_neighbor_heuristic(
                    vehicle_capacity, num_vehicles)
                if routes:
                    distance = self.calculate_routes_distance(routes)
                    print(
                        f"Heurística: Solución con {num_vehicles} vehículos, distancia {distance}")
                    return num_vehicles, routes

        # Si la heurística falla, usar el método exacto
        for num_vehicles in range(min_vehicles, len(self.ciudades)):
            routes, _ = self.solve_vrp(vehicle_capacity=vehicle_capacity,
                                       num_vehicles=num_vehicles,
                                       mipgap=0.2,
                                       time_limit=60)
            if routes:
                return num_vehicles, routes
        return None, None

    def find_min_capacity(self, num_vehicles):
        total_demand = sum(self.demands.values())
        min_capacity = math.ceil(total_demand / num_vehicles)

        # Primero intentar con la heurística
        if "vecino_cercano" in self.heuristics:
            for capacity in range(min_capacity, min_capacity + 50, 5):
                routes = self.nearest_neighbor_heuristic(
                    capacity, num_vehicles)
                if routes:
                    distance = self.calculate_routes_distance(routes)
                    print(
                        f"Heurística: Solución con capacidad {capacity}, distancia {distance}")
                    return capacity, routes

        # Si la heurística falla, usar el método exacto
        for capacity in range(min_capacity, min_capacity + 50, 5):
            routes, _ = self.solve_vrp(vehicle_capacity=capacity,
                                       num_vehicles=num_vehicles,
                                       mipgap=0.2,
                                       time_limit=60)
            if routes:
                return capacity, routes
        return None, None


def load_data(filename):
    ciudades = {}
    demands = {}
    with open(filename, 'r', encoding='utf-8') as f:
        next(f)  # Saltar la cabecera
        for line in f:
            parts = line.strip().split(';')
            if len(parts) >= 4:
                city_id = int(parts[0])
                x = float(parts[1])
                y = float(parts[2])
                demand = int(parts[3])
                ciudades[city_id] = (x, y)
                demands[city_id] = demand
    return ciudades, demands


def calculate_distances(ciudades):
    distancias = {}
    for i, (x1, y1) in ciudades.items():
        for j, (x2, y2) in ciudades.items():
            distancias[i, j] = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancias


def delta_time_mm_ss(delta):
    total_seconds = delta.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    return f"{minutes}m {seconds}s"


def main():
    # Cargar datos desde el archivo .csv ubicado en la carpeta medium-vrp
    ciudades, demands = load_data(r'ProyectoFinal/VRP/data/medium-vrp/vrp.csv')
    distancias = calculate_distances(ciudades)

    # Crear instancia VRP con heurísticas
    heuristics = ["vecino_cercano"]
    vrp = VRP(ciudades, distancias, demands, heuristics)

    # 1.1. Flota necesaria con capacidad de 100
    print("\n1.1. Flota necesaria con capacidad de 100:")
    num_vehicles, routes = vrp.find_min_vehicles(vehicle_capacity=100)
    print(f"Número mínimo de vehículos necesarios: {num_vehicles}")
    print("Rutas óptimas:")
    for i, route in enumerate(routes.values() if isinstance(routes, dict) else routes):
        print(f"Vehículo {i+1}: {route}")

    # 1.2. Capacidad necesaria para 4 rutas
    print("\n1.2. Capacidad necesaria para 4 rutas:")
    capacity, routes = vrp.find_min_capacity(num_vehicles=4)
    print(f"Capacidad mínima requerida: {capacity}")
    print("Rutas óptimas:")
    for i, route in enumerate(routes.values() if isinstance(routes, dict) else routes):
        print(f"Vehículo {i+1}: {route}")

    # 1.3. Punto de inviabilidad con capacidad de 150
    print("\n1.3. Punto de inviabilidad con capacidad máxima de 150:")
    total_demand = sum(demands.values())
    min_vehicles = math.ceil(total_demand / 150)
    print(
        f"El problema se vuelve inviable cuando se requieren más de {min_vehicles-1} vehículos")

    # Flota ideal para capacidad de 150
    print("\nFlota ideal para capacidad de 150:")
    num_vehicles, routes = vrp.find_min_vehicles(vehicle_capacity=150)
    print(f"Número ideal de vehículos: {num_vehicles}")
    print("Rutas óptimas:")
    for i, route in enumerate(routes.values() if isinstance(routes, dict) else routes):
        print(f"Vehículo {i+1}: {route}")


if __name__ == "__main__":
    main()

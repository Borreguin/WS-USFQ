import pyomo.environ as pyo
import numpy as np

class VRPModel:
    def __init__(self, coords, demands, vehicle_capacities):
        self.coords = coords
        self.num_nodes = len(coords)
        self.demands = demands
        self.vehicle_capacities = vehicle_capacities
        self.num_vehicles = len(vehicle_capacities)
        self.N = list(range(self.num_nodes))
        self.V = list(range(1, self.num_nodes))  # clientes sin el depósito
        self.K = list(range(self.num_vehicles))
        self.dist = {(i, j): np.linalg.norm(coords[i] - coords[j]) if i != j else 1e6
                     for i in self.N for j in self.N}
        self._build_model()

    def _build_model(self):
        model = pyo.ConcreteModel()

        model.N = pyo.Set(initialize=self.N)
        model.V = pyo.Set(initialize=self.V)
        model.K = pyo.Set(initialize=self.K)

        model.x = pyo.Var(model.N, model.N, model.K, within=pyo.Binary)
        model.u = pyo.Var(model.N, model.K, within=pyo.NonNegativeReals)

        # Función objetivo: minimizar distancia total
        model.obj = pyo.Objective(
            expr=sum(self.dist[i, j] * model.x[i, j, k]
                     for i in self.N for j in self.N for k in self.K if i != j),
            sense=pyo.minimize)

        # Cada cliente visitado una vez
        model.visit_once = pyo.ConstraintList()
        for j in self.V:
            model.visit_once.add(sum(model.x[i, j, k]
                                     for i in self.N if i != j for k in self.K) == 1)

        # Flujo de entrada = salida
        model.flow_balance = pyo.ConstraintList()
        for k in self.K:
            for h in self.N:
                model.flow_balance.add(sum(model.x[i, h, k] for i in self.N if i != h) ==
                                       sum(model.x[h, j, k] for j in self.N if j != h))

        # Salida única del depósito por vehículo
        model.depot_departure = pyo.ConstraintList()
        for k in self.K:
            model.depot_departure.add(sum(model.x[0, j, k] for j in self.V) <= 1)

        # Capacidad por vehículo
        model.capacity = pyo.ConstraintList()
        for k in self.K:
            model.capacity.add(
                sum(self.demands[j] * model.x[i, j, k]
                    for i in self.N for j in self.V if i != j) <= self.vehicle_capacities[k])

        # Subtour elimination (MTZ)
        M = self.num_nodes
        for k in self.K:
            for i in self.V:
                model.u[i, k].setlb(self.demands[i])
                model.u[i, k].setub(self.vehicle_capacities[k])
                for j in self.V:
                    if i != j:
                        model.add_component(f"mtz_{i}_{j}_{k}", pyo.Constraint(
                            expr=model.u[i, k] - model.u[j, k] +
                            self.vehicle_capacities[k] * model.x[i, j, k] <=
                            self.vehicle_capacities[k] - self.demands[j]))

        self.model = model

    def solve(self, solver_name='glpk'):
        solver = pyo.SolverFactory(solver_name)
        solver.solve(self.model, tee=True)

    def print_routes(self):
        model = self.model
        for k in self.K:
            print(f"\nRuta del vehículo {k}:")
            route = [0]
            current = 0
            visited = set()
            while True:
                for j in self.N:
                    if model.x[current, j, k].value is not None and pyo.value(model.x[current, j, k]) > 0.5:
                        route.append(j)
                        visited.add(j)
                        current = j
                        break
                else:
                    break
                if current == 0 or len(visited) >= len(self.V):
                    break
            print(" -> ".join(map(str, route + [0])))

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from collections import deque

import numpy as np
from scipy.spatial.distance import cdist
from collections import deque

import numpy as np
from scipy.spatial.distance import cdist
from collections import deque

class ClarkeWrightWithCapacities:
    def __init__(self, coords, demands, vehicle_capacities):
        self.coords = coords
        self.demands = demands
        self.vehicle_capacities = vehicle_capacities  # Lista con capacidad por vehículo
        self.num_nodes = len(coords)
        self.customers = list(range(1, self.num_nodes))
        self.routes = []
        self.distance_matrix = cdist(coords, coords)

    def savings_algorithm(self):
        # Calcular ahorros para cada par de clientes
        savings = []
        for i in self.customers:
            for j in self.customers:
                if i < j:
                    s = self.distance_matrix[0][i] + self.distance_matrix[0][j] - self.distance_matrix[i][j]
                    savings.append((s, i, j))
        savings.sort(reverse=True)

        # Inicializar una ruta para cada cliente
        customer_to_route = {}
        self.routes = []
        for i in self.customers:
            route = deque([i])
            load = self.demands[i]
            self.routes.append({'route': route, 'load': load})
            customer_to_route[i] = route

        # Fusionar rutas
        for _, i, j in savings:
            route_i = customer_to_route.get(i)
            route_j = customer_to_route.get(j)

            if route_i is None or route_j is None or route_i == route_j:
                continue

            r1 = next(r for r in self.routes if r['route'] == route_i)
            r2 = next(r for r in self.routes if r['route'] == route_j)

            total_load = r1['load'] + r2['load']
            if total_load > max(self.vehicle_capacities):
                continue

            # Unir extremos compatibles
            if route_i[-1] == i and route_j[0] == j:
                merged = deque(route_i)
                merged.extend(route_j)
            elif route_j[-1] == j and route_i[0] == i:
                merged = deque(route_j)
                merged.extend(route_i)
            else:
                continue

            # Crear nueva ruta fusionada
            self.routes.remove(r1)
            self.routes.remove(r2)
            self.routes.append({'route': merged, 'load': total_load})

            for client in merged:
                customer_to_route[client] = merged

            if len(self.routes) <= len(self.vehicle_capacities):
                break

        # Devolver rutas completas con depósito (0)
        return [[0] + list(r['route']) + [0] for r in self.routes]

    def print_routes(self):
        for idx, r in enumerate(self.routes):
            print(f"Vehículo {idx+1} (Carga: {r['load']}): 0 -> {' -> '.join(map(str, r['route']))} -> 0")



    def plot_routes(self):
        colors = plt.cm.get_cmap('tab10', len(self.routes))
        plt.figure(figsize=(8, 6))
        plt.scatter(self.coords[:, 0], self.coords[:, 1], c='black', s=40, label='Clientes')
        plt.scatter(self.coords[0, 0], self.coords[0, 1], c='red', s=100, marker='s', label='Depósito')

        for idx, r in enumerate(self.routes):
            route_coords = [self.coords[0]] + [self.coords[i] for i in r['route']] + [self.coords[0]]
            route_coords = np.array(route_coords)
            plt.plot(route_coords[:, 0], route_coords[:, 1], '-', label=f'Vehículo {idx+1}', color=colors(idx))

        plt.title('Rutas con Clarke-Wright Savings')
        plt.xlabel('Coordenada X')
        plt.ylabel('Coordenada Y')
        plt.legend(loc='best', fontsize='small', ncol=2)
        
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    def calculate_route_distances(self):
            """
            Retorna un diccionario con:
            - individual: distancias por ruta
            - total: distancia acumulada
            - average: distancia promedio
            """
            route_distances = []
            all_routes = [[0] + list(r['route']) + [0] for r in self.routes]
            for route in all_routes:
                distance = sum(np.linalg.norm(self.coords[route[i]] - self.coords[route[i + 1]])
                            for i in range(len(route) - 1))
                route_distances.append(distance)

            total_distance = sum(route_distances)
            average_distance = total_distance / len(route_distances) if route_distances else 0

            return {
                "individual": route_distances,
                "total": total_distance,
                "average": average_distance
            }

import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv('ProyectoFinal/VRP/data/large-vrp/vrp.csv', sep=';')

# Extraer coordenadas y demandas
coords = df[['X', 'Y']].values
demands = df['Demand'].tolist()

print(sum(demands))
# Capacidad de cada uno de los 10 vehículos (puedes ajustar)
vehicle_capacities = [120] * 10
def vrp_pyomo():
    # Crear y resolver el modelo
    vrp = VRPModel(coords, demands, vehicle_capacities)
    vrp.solve()


def find_capacities():
    # Número de vehículos disponibles (sin límite de capacidad)
    for i in range(1, 2000):
        n_vehicles = [i]*10
        vrp = ClarkeWrightWithCapacities(coords, demands, n_vehicles)
        vrp.savings_algorithm()
        if len(vrp.routes) == 10:
            print(f"Capacidad de {i} es suficiente para 10 vehículos")
            distances = vrp.calculate_route_distances()
            print("Distancias por ruta:", distances)
            vrp.plot_routes()

            break
    return vrp, n_vehicles, distances

vrp, _, _ = find_capacities()


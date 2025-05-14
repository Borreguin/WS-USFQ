import math
from collections import defaultdict
from typing import List, Dict, Tuple
import datetime as dt


class VRP:
    def __init__(self, ciudades, distancias, demands):
        self.ciudades = ciudades
        self.distancias = distancias
        self.demands = demands
        self.min_distance = self.get_min_distance()
        self.max_distance = self.get_max_distance()
        self.average_distance = self.get_average_distance()

    def get_min_distance(self):
        return min(d for d in self.distancias.values() if d > 0)

    def get_max_distance(self):
        return max(self.distancias.values())

    def get_average_distance(self):
        total = sum(self.distancias.values())
        count = len(self.distancias) - len(self.ciudades)  # Excluir diagonales
        return total / count

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

    def calculate_routes_distance(self, routes):
        total_distance = 0
        for route in routes:
            for i in range(len(route)-1):
                total_distance += self.distancias[route[i], route[i+1]]
        return total_distance

    def format_route_with_demands(self, route):
        """Formatea una ruta mostrando ID cliente y demanda"""
        formatted_route = []
        for node in route:
            if node == 0:  # Depósito
                formatted_route.append(f"Depósito (0)")
            else:
                formatted_route.append(
                    f"Cliente {node} (d:{self.demands[node]})")
        return formatted_route

    def find_min_vehicles(self, vehicle_capacity):
        """Encuentra el mínimo número de vehículos necesarios usando solo la heurística"""
        total_demand = sum(self.demands.values())
        min_vehicles = math.ceil(total_demand / vehicle_capacity)

        for num_vehicles in range(min_vehicles, len(self.ciudades)):
            routes = self.nearest_neighbor_heuristic(
                vehicle_capacity, num_vehicles)
            if routes:
                distance = self.calculate_routes_distance(routes)
                print(
                    f"Solución con {num_vehicles} vehículos, distancia total: {distance:.2f}")
                return num_vehicles, routes
        return None, None

    def find_min_capacity(self, num_vehicles):
        """Encuentra la mínima capacidad necesaria para un número fijo de vehículos usando solo la heurística"""
        total_demand = sum(self.demands.values())
        min_capacity = math.ceil(total_demand / num_vehicles)

        for capacity in range(min_capacity, min_capacity + 50, 5):
            routes = self.nearest_neighbor_heuristic(capacity, num_vehicles)
            if routes:
                distance = self.calculate_routes_distance(routes)
                print(
                    f"Solución con capacidad {capacity}, distancia total: {distance:.2f}")
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


def main():
    # Cargar datos desde el archivo .csv
    ciudades, demands = load_data(r'ProyectoFinal/VRP/data/medium-vrp/vrp.csv')
    distancias = calculate_distances(ciudades)

    # Crear instancia VRP
    vrp = VRP(ciudades, distancias, demands)

    # 1.1. Flota necesaria con capacidad de 100
    print("\n1.1. Flota necesaria con capacidad de 100:")
    num_vehicles, routes = vrp.find_min_vehicles(vehicle_capacity=100)
    if routes:
        print(f"Número mínimo de vehículos necesarios: {num_vehicles}")
        print("Rutas encontradas:")
        for i, route in enumerate(routes):
            formatted_route = vrp.format_route_with_demands(route)
            print(f"Vehículo {i+1}: {formatted_route}")
        total_distance = vrp.calculate_routes_distance(routes)
        print(f"Distancia total: {total_distance:.2f}")
    else:
        print("No se encontró solución factible")

    # 1.2. Capacidad necesaria para 4 rutas
    print("\n1.2. Capacidad necesaria para 4 rutas:")
    capacity, routes = vrp.find_min_capacity(num_vehicles=4)
    if routes:
        print(f"Capacidad mínima requerida: {capacity}")
        print("Rutas encontradas:")
        for i, route in enumerate(routes):
            formatted_route = vrp.format_route_with_demands(route)
            print(f"Vehículo {i+1}: {formatted_route}")
        total_distance = vrp.calculate_routes_distance(routes)
        print(f"Distancia total: {total_distance:.2f}")
    else:
        print("No se encontró solución factible")

    # 1.3. Punto de inviabilidad con capacidad de 150
    print("\n1.3. Punto de inviabilidad con capacidad máxima de 150:")
    total_demand = sum(demands.values())
    min_vehicles = math.ceil(total_demand / 150)
    print(
        f"El problema se vuelve inviable cuando se requieren menos de {min_vehicles-1} vehículos")

    # Flota ideal para capacidad de 150
    print("\nFlota ideal para capacidad de 150:")
    num_vehicles, routes = vrp.find_min_vehicles(vehicle_capacity=150)
    if routes:
        print(f"Número ideal de vehículos: {num_vehicles}")
        print("Rutas encontradas:")
        for i, route in enumerate(routes):
            formatted_route = vrp.format_route_with_demands(route)
            print(f"Vehículo {i+1}: {formatted_route}")
        total_distance = vrp.calculate_routes_distance(routes)
        print(f"Distancia total: {total_distance:.2f}")
    else:
        print("No se encontró solución factible")


if __name__ == "__main__":
    print("Modelo heurístico - solo vecinos cercanos")
    main()

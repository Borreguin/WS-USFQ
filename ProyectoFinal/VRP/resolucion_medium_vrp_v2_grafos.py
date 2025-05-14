import math
import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Dict, Tuple


class VRPVisualizer:
    def __init__(self, ciudades, distancias, demands):
        self.ciudades = ciudades
        self.distancias = distancias
        self.demands = demands
        self.colores_rutas = ['red', 'blue', 'green', 'purple',
                              'orange', 'brown', 'pink', 'gray',
                              'cyan', 'magenta', 'lime', 'indigo']

    def nearest_neighbor_heuristic(self, vehicle_capacity: int, num_vehicles: int = None):
        """Heurística del vecino más cercano para VRP"""
        unvisited = set(self.ciudades.keys()) - \
            {0}  # Todos los nodos excepto el depósito
        routes = []
        current_vehicles = 0

        if num_vehicles is None:
            total_demand = sum(self.demands.values())
            num_vehicles = math.ceil(total_demand / vehicle_capacity)

        while unvisited and current_vehicles < num_vehicles:
            current_load = 0
            current_location = 0  # Depósito
            route = [current_location]

            while unvisited and current_vehicles < num_vehicles:
                nearest = None
                min_dist = float('inf')

                for city in unvisited:
                    if self.demands[city] + current_load <= vehicle_capacity:
                        dist = self.distancias[current_location, city]
                        if dist < min_dist:
                            min_dist = dist
                            nearest = city

                if nearest is None:
                    break

                route.append(nearest)
                unvisited.remove(nearest)
                current_load += self.demands[nearest]
                current_location = nearest

            route.append(0)  # Volver al depósito
            routes.append(route)
            current_vehicles += 1

        return routes if not unvisited else None

    def calculate_routes_distance(self, routes):
        total_distance = 0
        for route in routes:
            for i in range(len(route)-1):
                total_distance += self.distancias[route[i], route[i+1]]
        return total_distance

    def plot_routes(self, routes, title="Rutas VRP"):
        plt.figure(figsize=(14, 10))
        G = nx.Graph()

        # Agregar nodos
        for city, (x, y) in self.ciudades.items():
            G.add_node(city, pos=(x, y), demand=self.demands[city])

        # Crear lista para la leyenda
        legend_elements = []
        # Para calcular demanda por vehículo
        vehicle_demands = [0] * len(routes)

        # Agregar aristas para cada ruta con colores diferentes
        for i, route in enumerate(routes):
            route_color = self.colores_rutas[i % len(self.colores_rutas)]
            # Calcular demanda total para esta ruta
            route_demand = sum(self.demands[node]
                               for node in route if node != 0)
            vehicle_demands[i] = route_demand

            for j in range(len(route)-1):
                G.add_edge(route[j], route[j+1], color=route_color, weight=2)

            # Añadir entrada a la leyenda para cada vehículo
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='w',
                                              markerfacecolor=route_color,
                                              markersize=10,
                                              label=f'Vehículo {i+1} (D: {route_demand})'))

        pos = nx.get_node_attributes(G, 'pos')
        demands = nx.get_node_attributes(G, 'demand')
        edge_colors = [G[u][v]['color'] for u, v in G.edges()]

        # Dibujar nodos (clientes)
        nx.draw_networkx_nodes(G, pos, node_size=200,
                               node_color='lightblue', label='Clientes')

        # Dibujar etiquetas de nodos
        nx.draw_networkx_labels(G, pos, font_size=8)

        # Dibujar demandas
        for node, (x, y) in pos.items():
            if node != 0:  # No mostrar demanda en el depósito
                plt.text(x, y+3, f'{demands[node]}', fontsize=8, ha='center',
                         bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))

        # Dibujar aristas
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=1.5)

        # Dibujar depósito especial con su propia leyenda
        nx.draw_networkx_nodes(G, pos, nodelist=[0], node_size=300,
                               node_color='yellow', label='Depósito')

        # Añadir leyenda general
        plt.legend(handles=[
            plt.Line2D([0], [0], marker='o', color='w',
                       markerfacecolor='yellow', markersize=10, label='Depósito'),
            plt.Line2D([0], [0], marker='o', color='w',
                       markerfacecolor='lightblue', markersize=10, label='Clientes')
        ] + legend_elements,
            loc='upper right', bbox_to_anchor=(1.25, 1), title="Leyenda")

        # Añadir título y nota explicativa
        plt.title(title, pad=20)
        plt.suptitle("Números en clientes = Demanda | D = Demanda total por ruta",
                     y=0.92, fontsize=10)

        # Mostrar estadísticas en la esquina inferior izquierda
        total_demand = sum(self.demands.values())
        plt.text(0.02, 0.02,
                 f"Demanda total: {total_demand}\nDistancia total: {self.calculate_routes_distance(routes):.2f}",
                 transform=plt.gca().transAxes,
                 bbox=dict(facecolor='white', alpha=0.8))

        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def solve_and_visualize(self, vehicle_capacity=None, num_vehicles=None, title="Rutas VRP"):
        routes = self.nearest_neighbor_heuristic(
            vehicle_capacity, num_vehicles)
        if routes:
            total_distance = self.calculate_routes_distance(routes)
            print(f"\nDistancia total: {total_distance:.2f}")
            print("Rutas encontradas:")
            for i, route in enumerate(routes):
                route_demand = sum(self.demands[node]
                                   for node in route if node != 0)
                print(f"Vehículo {i+1} (Demanda: {route_demand}): {route}")
            self.plot_routes(routes, title)
        else:
            print("No se encontró solución factible")
        return routes


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
    # Cargar datos
    ciudades, demands = load_data(r'ProyectoFinal/VRP/data/medium-vrp/vrp.csv')
    distancias = calculate_distances(ciudades)

    # Crear visualizador
    visualizador = VRPVisualizer(ciudades, distancias, demands)

    # 1.1. Flota necesaria con capacidad de 100
    print("\n1.1. Flota necesaria con capacidad de 100:")
    rutas_100 = visualizador.solve_and_visualize(
        vehicle_capacity=100,
        title="7 vehículos con capacidad 100"
    )

    # 1.2. Capacidad necesaria para 4 rutas
    print("\n1.2. Capacidad necesaria para 4 rutas:")
    total_demand = sum(demands.values())
    min_capacity = math.ceil(total_demand / 4)
    for capacity in range(min_capacity, min_capacity + 50, 5):
        rutas_4 = visualizador.solve_and_visualize(
            vehicle_capacity=capacity,
            num_vehicles=4,
            title=f"4 vehículos con capacidad {capacity}"
        )
        if rutas_4:
            break

    # 1.3. Flota ideal para capacidad de 150
    print("\nFlota ideal para capacidad de 150:")
    rutas_150 = visualizador.solve_and_visualize(
        vehicle_capacity=150,
        title="Flota ideal con capacidad 150"
    )


if __name__ == "__main__":
    print("Sistema de Optimización de Rutas VRP - Heurística de Vecino Más Cercano")
    main()

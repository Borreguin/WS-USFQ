#import libraries
import matplotlib.pyplot as plt
from collections import deque

import networkx as nx
from collections import deque

# Estado inicial y final
initial_state = ("L", "L", "L", "L")
goal_state = ("R", "R", "R", "R")

# Verifica si el estado es válido (sin comerse entre sí)
def is_valid(state):
    farmer, wolf, goat, cabbage = state
    if farmer != goat:
        if wolf == goat or goat == cabbage:
            return False
    return True

# Genera todos los estados vecinos válidos desde un estado
def get_neighbors(state):
    farmer, wolf, goat, cabbage = state
    neighbors = []
    opposite = {"L": "R", "R": "L"}

    options = [None, 'wolf', 'goat', 'cabbage']
    for carry in options:
        nf, nw, ng, nc = farmer, wolf, goat, cabbage
        nf = opposite[farmer]
        if carry == 'wolf' and farmer == wolf:
            nw = opposite[wolf]
        elif carry == 'goat' and farmer == goat:
            ng = opposite[goat]
        elif carry == 'cabbage' and farmer == cabbage:
            nc = opposite[cabbage]
        elif carry is None:
            pass
        else:
            continue
        new_state = (nf, nw, ng, nc)
        if is_valid(new_state):
            neighbors.append(new_state)
    return neighbors

# Búsqueda BFS para resolver el acertijo y construir el grafo
def solve_and_build_graph_bfs():
    G = nx.DiGraph()
    queue = deque()
    queue.append((initial_state, [initial_state]))
    visited = set()
    solution_path = []

    while queue:
        current_state, path = queue.popleft()
        G.add_node(current_state)
        if current_state == goal_state:
            solution_path = path
            break
        visited.add(current_state)
        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                G.add_node(neighbor)
                G.add_edge(current_state, neighbor)
                queue.append((neighbor, path + [neighbor]))

    return G, solution_path

# DFS para construir el grafo
def dfs_graph(current_state, path, visited, graph):
    if current_state == goal_state:
        return path
    visited.add(current_state)
    for neighbor in get_neighbors(current_state):
        if neighbor not in visited:
            graph.add_edge(current_state, neighbor)
            result = dfs_graph(neighbor, path + [neighbor], visited, graph)
            if result is not None:
                return result
    return None

# Resolver y construir grafo DFS
def solve_and_build_dfs_graph():
    visited = set()
    graph = nx.DiGraph()
    path = dfs_graph(initial_state, [initial_state], visited, graph)
    return graph, path

# Ejecutar solución y obtener grafo
graph, solution = solve_and_build_graph_bfs()
graph_dfs, solution_dfs = solve_and_build_dfs_graph()
# Posicionamiento de nodos
pos = nx.spring_layout(graph)

pos_dfs = nx.spring_layout(graph_dfs)

# Colorear nodos del camino solución
node_colors_bfs = ['lightgreen' if node in solution else 'lightgray' for node in graph.nodes()]
node_colors_dfs = ['lightgreen' if node in solution_dfs else 'lightgray' for node in graph_dfs.nodes()]

# Dibujar grafo bfs
plt.figure(figsize=(15, 10), num=0)
nx.draw(graph, pos, with_labels=True, node_size=1000, node_color=node_colors_bfs, font_size=8)
nx.draw_networkx_labels(graph, pos, labels={node: f"{node}" for node in graph.nodes()}, font_size=8)
plt.title("Solución al acertijo del granjero: grafo de estados", fontsize=14)
plt.axis('off')
plt.savefig("acertijo_granjero_bfs.png", dpi=300, bbox_inches='tight')
plt.show()


plt.figure(figsize=(15, 10), num=1)
nx.draw(graph_dfs, pos_dfs, with_labels=True, node_size=1000, node_color=node_colors_dfs, font_size=8)
nx.draw_networkx_labels(graph_dfs, pos_dfs, labels={node: f"{node}" for node in graph_dfs.nodes()}, font_size=8)
plt.title("Solución al acertijo del granjero: grafo de estados", fontsize=14)
plt.axis('off')
plt.show()
plt.savefig("acertijo_granjero_dfs.png", dpi=300, bbox_inches='tight')





if __name__ == '__main__':
    print("Implementa el código aquí")
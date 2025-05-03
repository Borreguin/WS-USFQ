import time
import networkx as nx
import matplotlib.pyplot as plt


def define_color(cell):
    if cell == '#':
        return 'black'
    elif cell == ' ':   # Espacio vacío
        return 'white'
    elif cell == 'E':   # Entrada
        return 'green'
    elif cell == 'S':   # Salida
        return 'red'

# Grafico del labrinto como grafo
def draw_graph(graph):
    pos = {node: (node[1], -node[0]) for node in graph.nodes()}  # Invertir eje Y para que coincida con el laberinto
    nx.draw(graph, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=8, font_color="black")
    plt.title("Grafo del Laberinto")
    plt.show()


def bfs_search(graph, start, goal):
    start_time = time.time()
    queue = [(start, [start])]
    while queue:
        (node, path) = queue.pop(0)
        for neighbor in graph.neighbors(node):
            if neighbor not in path:
                if neighbor == goal:
                    end_time = time.time()
                    print(f"BFS Time: {end_time - start_time:.4f} seconds")
                    return path + [neighbor]
                queue.append((neighbor, path + [neighbor]))
    return None

def dfs_search(graph, start, goal):
    start_time = time.time()
    stack = [(start, [start])]
    while stack:
        (node, path) = stack.pop()
        for neighbor in graph.neighbors(node):
            if neighbor not in path:
                if neighbor == goal:
                    end_time = time.time()
                    print(f"DFS Time: {end_time - start_time:.4f} seconds")
                    return path + [neighbor]
                stack.append((neighbor, path + [neighbor]))
    return None

def astar_search(graph, start, goal):
    start_time = time.time()
    def heuristic(node1, node2):
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])  # Manhattan distance

    open_set = [(0, start, [start])]
    while open_set:
        open_set.sort()
        _, current, path = open_set.pop(0)
        if current == goal:
            end_time = time.time()
            print(f"A* Time: {end_time - start_time:.4f} seconds")
            return path
        for neighbor in graph.neighbors(current):
            if neighbor not in path:
                g_cost = len(path)
                h_cost = heuristic(neighbor, goal)
                open_set.append((g_cost + h_cost, neighbor, path + [neighbor]))
    return None

def nearest_neighbor_search(graph, start, goal):
    start_time = time.time()
    current = start
    path = [current]
    while current != goal:
        neighbors = list(graph.neighbors(current))
        if not neighbors:
            break
        current = min(neighbors, key=lambda n: abs(n[0] - goal[0]) + abs(n[1] - goal[1]))
        path.append(current)
    end_time = time.time()
    print(f"Nearest Neighbor Time: {end_time - start_time:.4f} seconds")
    return path if path[-1] == goal else None


def nayfeth_search(graph, start, goal):
    start_time = time.time()
    current = start
    path = [current]
    visited = set()
    visited.add(current)

    while current != goal:
        neighbors = list(graph.neighbors(current))
        if not neighbors:
            break  # No hay más vecinos transitables

        # Seleccionar el vecino más cercano al objetivo
        current = min(
            (n for n in neighbors if n not in visited),
            key=lambda n: abs(n[0] - goal[0]) + abs(n[1] - goal[1]),
            default=None
        )

        if current is None:
            break  # No hay más caminos disponibles

        path.append(current)
        visited.add(current)

    end_time = time.time()
    print(f"Nayfeth Time: {end_time - start_time:.4f} seconds")
    return path if path[-1] == goal else None


# Graficar solucion en el laberinto
def plot_solution_on_maze(maze, solution, title="Maze Solution"):
            height = len(maze.maze)
            width = len(maze.maze[0])
            fig = plt.figure(figsize=(width / 4, height / 4))
            for y in range(height):
                for x in range(width):
                    cell = maze.maze[y][x]
                    color = define_color(cell)
                    plt.fill([x, x + 1, x + 1, x], [y, y, y + 1, y + 1], color=color, edgecolor='black')

            # Dibujar la solución
            for i in range(len(solution) - 1):
                y1, x1 = solution[i]
                y2, x2 = solution[i + 1]
                plt.plot([x1 + 0.5, x2 + 0.5], [y1 + 0.5, y2 + 0.5], color='red', linewidth=2)

            plt.xlim(0, width)
            plt.ylim(0, height)
            plt.gca().invert_yaxis()
            plt.xticks([])
            plt.yticks([])
            fig.tight_layout()
            plt.title(title)
            plt.show()


# Graficar la solución en el grafo
def plot_solution_on_graph(graph, solution, title="Graph Solution"):
    pos = {node: (node[1], -node[0]) for node in graph.nodes()}
    nx.draw(graph, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=8, font_color="black")
    path_edges = list(zip(solution, solution[1:]))
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2)
    plt.title(title)
    plt.show()
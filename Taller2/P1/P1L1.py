import os
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
import heapq

from P1_util import define_color

class MazeLoader:
    def __init__(self, filename):
        self.filename = filename
        self.maze = None

    def load_Maze(self):
        _maze = []
        with open(self.filename, 'r') as file:
            for line in file:
                _maze.append(list(line.strip()))
        self.maze = _maze
        return self

    def plot_maze(self, path_bfs=None, path_astar=None):
        height = len(self.maze)
        width = len(self.maze[0])

        fig, ax = plt.subplots(figsize=(width / 3, height / 3))

        for y in range(height):
            for x in range(width):
                cell = self.maze[y][x]
                color = define_color(cell)
                ax.fill([x, x + 1, x + 1, x], [y, y, y + 1, y + 1], color=color, edgecolor='black')

        def draw_path(path, color):
            if not path:
                return
            for (x, y) in path:
                ax.fill([x, x + 1, x + 1, x], [y, y, y + 1, y + 1], color=color, alpha=0.4)

        draw_path(path_bfs, 'blue')
        draw_path(path_astar, 'orange')

        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        ax.invert_yaxis()
        ax.set_xticks([])
        ax.set_yticks([])
        plt.tight_layout()
        plt.show()
        return self

    def get_graph(self):
        if self.maze is None:
            raise ValueError("Maze not loaded")

        G = nx.Graph()
        height = len(self.maze)
        width = len(self.maze[0])

        for y in range(height):
            for x in range(width):
                if self.maze[y][x] in [' ', 'E', 'S']:
                    current_node = (x, y)
                    G.add_node(current_node)

                    for dx, dy in [(1, 0), (0, 1)]:
                        nx_, ny_ = x + dx, y + dy
                        if 0 <= nx_ < width and 0 <= ny_ < height:
                            if self.maze[ny_][nx_] in [' ', 'E', 'S']:
                                G.add_edge(current_node, (nx_, ny_))
        return G

# Algoritmos de búsqueda
def bfs(graph, start, goal):
    queue = deque([[start]])
    visited = set()

    while queue:
        path = queue.popleft()
        node = path[-1]
        if node in visited:
            continue
        visited.add(node)
        if node == goal:
            return path
        for neighbor in graph.neighbors(node):
            queue.append(path + [neighbor])
    return None

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(graph, start, goal):
    queue = [(heuristic(start, goal), 0, [start])]
    visited = set()

    while queue:
        est_total, cost, path = heapq.heappop(queue)
        node = path[-1]
        if node in visited:
            continue
        visited.add(node)
        if node == goal:
            return path
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                new_cost = cost + 1
                heapq.heappush(queue, (new_cost + heuristic(neighbor, goal), new_cost, path + [neighbor]))
    return None

def find_start_end(maze):
    start = end = None
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 'E':
                start = (x, y)
            elif cell == 'S':
                end = (x, y)
    return start, end

# Función principal
def resolver_laberinto(archivo):
    loader = MazeLoader(archivo).load_Maze()
    graph = loader.get_graph()
    start, end = find_start_end(loader.maze)

    path_bfs = bfs(graph, start, end)
    path_astar = astar(graph, start, end)

    print(f"\n→ Resultados para {archivo}:")
    print(f"BFS pasos: {len(path_bfs) if path_bfs else 'No encontrado'}")
    print(f"A* pasos: {len(path_astar) if path_astar else 'No encontrado'}")

    loader.plot_maze(path_bfs, path_astar)

if __name__ == '__main__':
    resolver_laberinto(os.path.join(os.path.dirname(__file__), 'laberinto1.txt'))
    # Puedes cambiar a 'laberinto2.txt' o 'laberinto3.txt'
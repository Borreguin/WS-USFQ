import matplotlib.pyplot as plt
import os, sys
project_path = os.path.dirname(__file__)
sys.path.append(project_path)

from P1_util import define_color

class MazeLoader:
    def __init__(self, filename):
        self.filename = filename
        self.maze = None

    def load_Maze(self):
        _maze = []
        file_path = os.path.join(project_path, self.filename)
        print("Loading Maze from", file_path)
        with open(file_path, 'r') as file:
            for line in file:
                _maze.append(list(line.strip()))
        self.maze = _maze
        return self

    def plot_maze(self):
        height = len(self.maze)
        width = len(self.maze[0])

        fig = plt.figure(figsize=(width/4, height/4))  # Ajusta el tamaño de la figura según el tamaño del Maze
        for y in range(height):
            for x in range(width):
                cell = self.maze[y][x]
                color = define_color(cell)
                plt.fill([x, x+1, x+1, x], [y, y, y+1, y+1], color=color, edgecolor='black')

        plt.xlim(0, width)
        plt.ylim(0, height)
        plt.gca().invert_yaxis()  # Invierte el eje y para que el origen esté en la esquina inferior izquierda
        plt.xticks([])
        plt.yticks([])
        fig.tight_layout()
        plt.show()
        return self

    def get_graph(self):
        # Implementar la creación del grafo a partir del laberinto
        return None

import networkx as nx

def get_graph(self):
        if self.maze is None:
            raise ValueError("Maze not loaded")

        G = nx.Graph()
        height = len(self.maze)
        width = len(self.maze[0])

        for y in range(height):
            for x in range(width):
                current_cell = self.maze[y][x]
                if current_cell in [' ', 'E', 'S']:
                    current_node = (x, y)
                    G.add_node(current_node)

                    # Verificar vecinos: derecha y abajo (evita duplicar aristas)
                    for dx, dy in [(1, 0), (0, 1)]:
                        nx_, ny_ = x + dx, y + dy
                        if 0 <= nx_ < width and 0 <= ny_ < height:
                            neighbor_cell = self.maze[ny_][nx_]
                            if neighbor_cell in [' ', 'E', 'S']:
                                neighbor_node = (nx_, ny_)
                                G.add_edge(current_node, neighbor_node)

        return G

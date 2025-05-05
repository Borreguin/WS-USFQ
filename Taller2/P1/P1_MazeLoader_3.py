import matplotlib.pyplot as plt
import os, sys
import networkx as nx
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

    def plot_maze(self, path = None, show_graph = False):
        height = len(self.maze)
        width = len(self.maze[0])

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_xlim(-0.5, width - 0.5)
        ax.set_ylim(-height + 0.5, 0.5)
        ax.set_aspect('equal')
        ax.grid(True) # Ajusta el tamaño de la figura según el tamaño del Maze
        for y in range(height):
            for x in range(width):
                cell = self.maze[y][x]
                color = define_color(cell)
                rect = plt.Rectangle((x -.5, -y - .5), 1, 1, facecolor=color, edgecolor='black')
                ax.add_patch(rect)

        
        plt.gca().invert_yaxis()  # Invierte el eje y para que el origen esté en la esquina inferior izquierda
        ax.set_xticks([])
        ax.set_yticks([])
        self.graph = self.get_graph()
        plt.title("Maze")
        if show_graph:
            pos = {(r, c): (c, -r) for r in range(height) for c in range(width) if self.maze[r][c] != '#'}
            # Draw only edges and small nodes for clarity
            nx.draw_networkx_edges(self.graph, pos, ax=ax, edge_color='gray', width=0.5)
            nx.draw_networkx_nodes(self.graph, pos, ax=ax, node_color='lightblue', node_size=15)
        if path:
            pos = {(r, c): (c, -r) for r in range(height) for c in range(width) if self.maze[r][c] != '#'}
            nx.draw_networkx_nodes(self.graph, pos, ax=ax, nodelist=path, node_color='yellow', node_size=30)
            nx.draw_networkx_edges(self.graph, pos, ax=ax, edgelist=list(zip(path[:-1], path[1:])), edge_color='orange', width=2)

        plt.tight_layout()
        plt.show()
        return self

    def get_graph(self):
        # Implementar la creación del grafo a partir del laberinto
        rows, cols = len(self.maze), len(self.maze[0])
        G = nx.Graph()
        
        # Movement directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for r in range(rows):
            for c in range(cols):
                if self.maze[r][c] != '#':  # Current cell is walkable
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        # Check neighbor bounds and if it's walkable
                        if 0 <= nr < rows and 0 <= nc < cols and self.maze[nr][nc] != '#':
                            G.add_edge((r, c), (nr, nc))
        
        return G

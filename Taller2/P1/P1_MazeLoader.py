import matplotlib.pyplot as plt
import os, sys
import time
import networkx as nx

project_path = os.path.dirname(__file__)
sys.path.append(project_path)


#from Taller2.P1.P1_util import define_color
from P1_util import *


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
        plt.title("Laberinto")
        plt.show()
        return self

    def get_graph(self):
        G = nx.DiGraph() # Grafo dirigido
        
        # Dimensiones del laberinto
        height = len(self.maze)
        width = len(self.maze[0])
        
        # Función para verificar si una celda es transitable
        def is_walkable(cell):
            return cell in [' ', 'E', 'S']  # Espacio vacío, entrada o salida
        
        # Agregar nodos y aristas al grafo
        for y in range(height):
            for x in range(width):
                if is_walkable(self.maze[y][x]):
                    # Agregar nodo para la celda actual
                    G.add_node((y, x), value=self.maze[y][x])
                    
                    # Verificar celdas adyacentes (arriba, abajo, izquierda, derecha)
                    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        my, mx = y + dy, x + dx
                        if 0 <= my < height and 0 <= mx < width and is_walkable(self.maze[my][mx]):
                            # Agregar arista entre la celda actual y la celda adyacente
                            G.add_edge((y, x), (my, mx))
        
        return G


import matplotlib.pyplot as plt
import os, sys
project_path = os.path.dirname(__file__)
sys.path.append(project_path)
from Taller2.P1.P1_util import define_color

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

        fig = plt.figure(figsize=(width/4, height/4))
        for y in range(height):
            for x in range(width):
                cell = self.maze[y][x]
                color = define_color(cell)
                plt.fill([x, x+1, x+1, x], [y, y, y+1, y+1], color=color, edgecolor='black')

        plt.xlim(0, width)
        plt.ylim(0, height)
        plt.gca().invert_yaxis()
        plt.xticks([])
        plt.yticks([])
        fig.tight_layout()
        plt.show()
        return self

    def get_graph(self):
        graph = {}
        start = None
        end = None
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                if self.maze[y][x] in [' ', 'E', 'S']:
                    neighbors = []
                    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < len(self.maze) and 0 <= nx < len(self.maze[0]):
                            if self.maze[ny][nx] in [' ', 'E', 'S']:
                                neighbors.append((ny, nx))
                    graph[(y, x)] = neighbors
                    if self.maze[y][x] == 'E':
                        start = (y, x)
                    elif self.maze[y][x] == 'S':
                        end = (y, x)
        if start is None or end is None:
            print("ERROR: No se encontró 'E' o 'S'")
            return None
        return graph, start, end


import os, sys
project_path = os.path.dirname(__file__)
sys.path.append(project_path)
from P1_MazeLoader import MazeLoader
from P1_util import define_color

import networkx as nx
import matplotlib.pyplot as plt

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def dijkstra_path(G, start, end):
    return nx.dijkstra_path(G, start, end)

def astar_path(G, start, end):
    return nx.astar_path(G, start, end, heuristic=heuristic)

def draw_path_on_maze(maze_obj, path):
    maze_copy = [row[:] for row in maze_obj.maze]
    for (x, y) in path:
        if maze_copy[y][x] not in ['E', 'S']:
            maze_copy[y][x] = '.'

    # Mostrar laberinto con camino
    height = len(maze_copy)
    width = len(maze_copy[0])
    fig = plt.figure(figsize=(width / 4, height / 4))
    for y in range(height):
        for x in range(width):
            cell = maze_copy[y][x]
            color = define_color(cell) if cell != '.' else 'blue'
            plt.fill([x, x+1, x+1, x], [y, y, y+1, y+1], color=color, edgecolor='black')
    plt.gca().invert_yaxis()
    plt.xticks([])
    plt.yticks([])
    plt.title("Camino encontrado")
    fig.tight_layout()
    plt.show()



def study_case_1():
    print("This is study case 1")
    maze_file = 'laberinto1.txt'
    maze = MazeLoader(maze_file).load_Maze().plot_maze()
    # Aquí la implementación de la solución:
    graph = maze.get_graph()



def study_case_2():
    print("This is study case 2")
    maze_file = 'laberinto2.txt'
    maze = MazeLoader(maze_file).load_Maze().plot_maze()
    # Aquí la implementación de la solución:
    graph = maze.get_graph()


def study_case_3():
    print("This is study case 3")
    maze_file = 'laberinto3.txt'
    maze = MazeLoader(maze_file).load_Maze().plot_maze()
    graph, start, end = maze.get_graph()

    print("Usando Dijkstra...")
    path_dijkstra = dijkstra_path(graph, start, end)
    draw_path_on_maze(maze, path_dijkstra)

    print("Usando A*...")
    path_astar = astar_path(graph, start, end)
    draw_path_on_maze(maze, path_astar)


if __name__ == '__main__':
    study_case_3()

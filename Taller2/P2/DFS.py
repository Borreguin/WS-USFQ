import os, sys
from collections import deque
import matplotlib.pyplot as plt

project_path = os.path.dirname(__file__)
sys.path.append(project_path)
from P1_MazeLoader import MazeLoader
from Taller2.P1.P1_util import define_color

def dfs(graph, start, goal):
    stack = [[start]]
    visited = set()
    while stack:
        path = stack.pop()
        node = path[-1]
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                stack.append(new_path)
    return None

def plot_dfs_solution(maze_data, path):
    height = len(maze_data)
    width = len(maze_data[0])
    fig = plt.figure(figsize=(width/4, height/4))
    ax = plt.gca()

    for y in range(height):
        for x in range(width):
            cell = maze_data[y][x]
            base_color = define_color(cell)
            plt.fill([x, x+1, x+1, x], [y, y, y+1, y+1], color=base_color, edgecolor='black')

    for y, x in path:
        plt.fill([x, x+1, x+1, x], [y, y, y+1, y+1], color='magenta', edgecolor='black')

    plt.title("DFS Path")
    plt.xlim(0, width)
    plt.ylim(0, height)
    ax.invert_yaxis()
    plt.xticks([])
    plt.yticks([])
    fig.tight_layout()
    plt.show()

def study_case_3():
    print("This is study case 3")
    maze_file = 'laberinto3.txt'
    loader = MazeLoader(maze_file).load_Maze()
    loader.plot_maze()
    result = loader.get_graph()
    if result is None:
        return
    graph, start, goal = result

    print(f"Start: {start}, Goal: {goal}")

    print("Solving maze using DFS...")
    path_dfs = dfs(graph, start, goal)
    if path_dfs:
        print("DFS Path length:", len(path_dfs))
        plot_dfs_solution(loader.maze, path_dfs)
    else:
        print("No path found by DFS.")

if __name__ == '__main__':
    study_case_3()

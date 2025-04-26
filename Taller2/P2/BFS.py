import os, sys
from collections import deque
import matplotlib.pyplot as plt

project_path = os.path.dirname(__file__)
sys.path.append(project_path)
from P1_MazeLoader import MazeLoader
from Taller2.P1.P1_util import define_color

def bfs(graph, start, goal):
    queue = deque([[start]])
    visited = set()
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    return None

def plot_solution(maze_data, path):
    height = len(maze_data)
    width = len(maze_data[0])
    fig = plt.figure(figsize=(width/4, height/4))
    for y in range(height):
        for x in range(width):
            cell = maze_data[y][x]
            color = define_color(cell)
            plt.fill([x, x+1, x+1, x], [y, y, y+1, y+1], color=color, edgecolor='black')
    for (y, x) in path:
        plt.fill([x, x+1, x+1, x], [y, y, y+1, y+1], color='cyan', edgecolor='black')
    plt.xlim(0, width)
    plt.ylim(0, height)
    plt.gca().invert_yaxis()
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
    path = bfs(graph, start, goal)
    if path:
        print("Path found! Visualizing...")
        plot_solution(loader.maze, path)
    else:
        print("No path found.")

if __name__ == '__main__':
    study_case_3()

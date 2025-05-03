import os, sys
project_path = os.path.dirname(__file__)
sys.path.append(project_path)

#from P1_MazeLoader import MazeLoader
from P1_MazeLoader import *


def study_case_1():
    print("This is study case 1")
    maze_file = 'laberinto1.txt'
    maze = MazeLoader(maze_file).load_Maze().plot_maze()

    # Aquí la implementación de la solución:
    graph = maze.get_graph()
    draw_graph(graph)

    start = (1, 1)
    goal = (7, 9)
    print("Start:", start)
    print("Goal:", goal)

    bfs_solucion = bfs_search(graph, start, goal)
    print("BFS Solution:", bfs_solucion)
    plot_solution_on_maze(maze, bfs_solucion, title="Maze BFS Solution")
    plot_solution_on_graph(graph, bfs_solucion, title="Graph BFS Solution")

    dfs_solucion = dfs_search(graph, start, goal)
    print("DFS Solution:", dfs_solucion)
    plot_solution_on_maze(maze, dfs_solucion, title="Maze DFS Solution")
    plot_solution_on_graph(graph, dfs_solucion, title="Graph DFS Solution")

    astar_solucion = astar_search(graph, start, goal)
    print("A* Solution:", astar_solucion)
    plot_solution_on_maze(maze, astar_solucion, title="Maze A* Solution")
    plot_solution_on_graph(graph, astar_solucion, title="Graph A* Solution")

    print("Nearest Neighbor Solution: None")
    #nearest_neighbor_solucion = nearest_neighbor_search(graph, start, goal)
    #print("Nearest Neighbor Solution:", nearest_neighbor_solucion)
    #plot_solution_on_maze(maze, nearest_neighbor_solucion, title="Maze Nearest Neighbor Solution")
    #plot_solution_on_graph(graph, nearest_neighbor_solucion, title="Graph Nearest Neighbor Solution")

    nayfeth_solucion = nayfeth_search(graph, start, goal)
    print("Nayfeth Solution:", nayfeth_solucion)
    plot_solution_on_maze(maze, nayfeth_solucion, title="Maze Nayfeth Solution")
    plot_solution_on_graph(graph, nayfeth_solucion, title="Graph Nayfeth Solution")





def study_case_2():
    print("This is study case 2")
    maze_file = 'laberinto2.txt'
    maze = MazeLoader(maze_file).load_Maze().plot_maze()

    # Aquí la implementación de la solución:
    graph = maze.get_graph()
    draw_graph(graph)

    start = (1, 1)
    goal = (13, 27)
    print("Start:", start)
    print("Goal:", goal)

    bfs_solucion = bfs_search(graph, start, goal)
    print("BFS Solution:", bfs_solucion)
    plot_solution_on_maze(maze, bfs_solucion, title="Maze BFS Solution")
    plot_solution_on_graph(graph, bfs_solucion, title="Graph BFS Solution")

    dfs_solucion = dfs_search(graph, start, goal)
    print("DFS Solution:", dfs_solucion)
    plot_solution_on_maze(maze, dfs_solucion, title="Maze DFS Solution")
    plot_solution_on_graph(graph, dfs_solucion, title="Graph DFS Solution")

    astar_solucion = astar_search(graph, start, goal)
    print("A* Solution:", astar_solucion)
    plot_solution_on_maze(maze, astar_solucion, title="Maze A* Solution")
    plot_solution_on_graph(graph, astar_solucion, title="Graph A* Solution")

    print("Nearest Neighbor Solution: None")
    #nearest_neighbor_solucion = nearest_neighbor_search(graph, start, goal)
    #print("Nearest Neighbor Solution:", nearest_neighbor_solucion)
    #plot_solution_on_maze(maze, nearest_neighbor_solucion, title="Maze Nearest Neighbor Solution")
    #plot_solution_on_graph(graph, nearest_neighbor_solucion, title="Graph Nearest Neighbor Solution")

    nayfeth_solucion = nayfeth_search(graph, start, goal)
    if nayfeth_solucion is None:
        print("Nayfeth Solution: None")
    else:
        print("Nayfeth Solution:", nayfeth_solucion)
        plot_solution_on_maze(maze, nayfeth_solucion, title="Maze Nayfeth Solution")
        plot_solution_on_graph(graph, nayfeth_solucion, title="Graph Nayfeth Solution")

    



def study_case_3():
    print("This is study case 2")
    maze_file = 'laberinto3.txt'
    maze = MazeLoader(maze_file).load_Maze().plot_maze()

    # Aquí la implementación de la solución:
    graph = maze.get_graph()
    draw_graph(graph)

    start = (2, 4)
    goal = (20, 104)
    print("Start:", start)
    print("Goal:", goal)

    print("BFS Solution: None")
    #bfs_solucion = bfs_search(graph, start, goal)
    #print("BFS Solution:", bfs_solucion)
    #plot_solution_on_maze(maze, bfs_solucion, title="Maze BFS Solution")
    #plot_solution_on_graph(graph, bfs_solucion, title="Graph BFS Solution")

    dfs_solucion = dfs_search(graph, start, goal)
    print("DFS Solution:", dfs_solucion)
    plot_solution_on_maze(maze, dfs_solucion, title="Maze DFS Solution")
    plot_solution_on_graph(graph, dfs_solucion, title="Graph DFS Solution")

    print("A* Solution: None")
    #astar_solucion = astar_search(graph, start, goal)
    #print("A* Solution:", astar_solucion)
    #plot_solution_on_maze(maze, astar_solucion, title="Maze A* Solution")
    #plot_solution_on_graph(graph, astar_solucion, title="Graph A* Solution")

    print("Nearest Neighbor Solution: None")
    #nearest_neighbor_solucion = nearest_neighbor_search(graph, start, goal)
    #print("Nearest Neighbor Solution:", nearest_neighbor_solucion)
    #plot_solution_on_maze(maze, nearest_neighbor_solucion, title="Maze Nearest Neighbor Solution")
    #plot_solution_on_graph(graph, nearest_neighbor_solucion, title="Graph Nearest Neighbor Solution")

    nayfeth_solucion = nayfeth_search(graph, start, goal)
    if nayfeth_solucion is None:
        print("Nayfeth Solution: None")
    else:
        print("Nayfeth Solution:", nayfeth_solucion)
        plot_solution_on_maze(maze, nayfeth_solucion, title="Maze Nayfeth Solution")
        plot_solution_on_graph(graph, nayfeth_solucion, title="Graph Nayfeth Solution")


if __name__ == '__main__':
    study_case_1()
    study_case_2()
    study_case_3()

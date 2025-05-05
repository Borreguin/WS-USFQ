import os, sys
import time
from collections import deque
from heapq import heappop, heappush
import matplotlib.pyplot as plt

project_path = os.path.dirname(__file__)
sys.path.append(project_path)

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Algoritmos de búsqueda

def bfs(graph, start, end):
    queue = deque([(start, [start])])
    visited = set()
    start_time = time.time()
    
    while queue:
        (vertex, path) = queue.popleft()
        if vertex not in visited:
            if vertex == end:
                end_time = time.time()
                print(f"BFS tiempo de ejecución: {end_time - start_time:.6f} segundos")
                return path, end_time - start_time
            visited.add(vertex)
            for neighbor in graph[vertex]:
                queue.append((neighbor, path + [neighbor]))
    
    end_time = time.time()
    print(f"BFS tiempo de ejecución: {end_time - start_time:.6f} segundos")
    return [], end_time - start_time

def dfs(graph, start, end):
    stack = [(start, [start])]
    visited = set()
    start_time = time.time()
    
    while stack:
        (vertex, path) = stack.pop()
        if vertex not in visited:
            if vertex == end:
                end_time = time.time()
                print(f"DFS tiempo de ejecución: {end_time - start_time:.6f} segundos")
                return path, end_time - start_time
            visited.add(vertex)
            for neighbor in graph[vertex]:
                stack.append((neighbor, path + [neighbor]))
    
    end_time = time.time()
    print(f"DFS tiempo de ejecución: {end_time - start_time:.6f} segundos")
    return [], end_time - start_time

def dijkstra(graph, start, end):
    heap = [(0, start, [start])]
    visited = set()
    start_time = time.time()
    
    while heap:
        cost, node, path = heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        if node == end:
            end_time = time.time()
            print(f"Dijkstra tiempo de ejecución: {end_time-start_time:.6f} segundos")
            return path, end_time - start_time
        for neighbor in graph[node]:
            if neighbor not in visited:
                heappush(heap, (cost + 1, neighbor, path + [neighbor]))
    
    end_time = time.time()
    print(f"Dijkstra tiempo de ejecución: {end_time-start_time:.6f} segundos")
    return [], end_time - start_time

def a_star(graph, start, end):
    open_set = [(0 + manhattan_distance(start, end), 0, start, [start])]
    visited = set()
    start_time = time.time()

    while open_set:
        f, g, current, path = heappop(open_set)
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            end_time = time.time()
            print(f"A* tiempo de ejecución: {end_time - start_time:.6f} segundos")
            return path, end_time - start_time

        for neighbor in graph[current]:
            if neighbor not in visited:
                new_g = g + 1
                new_f = new_g + manhattan_distance(neighbor, end)
                heappush(open_set, (new_f, new_g, neighbor, path + [neighbor]))

    end_time = time.time()
    print(f"A* tiempo de ejecución: {end_time - start_time:.6f} segundos")
    return [], end_time - start_time

def visualize_results(maze, bfs_path, dfs_path, dijkstra_path, a_star_path, evaluation_results, maze_file):
    """Visualize maze and algorithm performance comparison"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 1. Plot the maze with paths
    maze.plot_paths({
        'BFS': bfs_path,
        'DFS': dfs_path,
        'Dijkstra': dijkstra_path,
        'A*': a_star_path
    }, ax1)
    
    ax1.set_title(f"Maze: {maze_file}")
    
    # 2. Plot performance comparison
    algorithms = list(evaluation_results.keys())
    path_lengths = [evaluation_results[algo]["path_length"] for algo in algorithms]
    execution_times = [evaluation_results[algo]["execution_time"] * 1000 for algo in algorithms]  # Convert to ms

    x = range(len(algorithms))
    width = 0.35

    # Path length bars
    ax2.bar([i - width/2 for i in x], path_lengths, width, label='Longitud del camino', color='skyblue')

    # Execution time bars
    ax2.bar([i + width/2 for i in x], execution_times, width, label='Tiempo de ejecución (ms)', color='red')

    ax2.set_xlabel("Algoritmo")
    ax2.set_ylabel("Valor")
    ax2.set_title("Comparación de rendimiento")
    ax2.set_xticks(x)
    ax2.set_xticklabels(algorithms)
    ax2.legend()
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.show()


def study_case_1():
    from P1_MazeLoader import MazeLoader
    print('-'*30,"\nThis is study case 1\n",'-'*30)
    maze_file = 'laberinto1.txt'
    maze = MazeLoader(maze_file).load_Maze().plot_maze()
    # Aquí la implementación de la solución:
    graph = maze.get_graph(visualize=True)
    
    # Get start and end positions from the maze
    start_node = maze.start
    end_node = maze.end
    print(f"Start: {start_node}, End: {end_node}")
    
    # Run all search algorithms
    print("\nEjecutando algoritmos de búsqueda...")
    bfs_path, bfs_time = bfs(graph, start_node, end_node)
    dfs_path, dfs_time = dfs(graph, start_node, end_node)
    dijkstra_path, dijkstra_time = dijkstra(graph, start_node, end_node)
    a_star_path, a_star_time = a_star(graph, start_node, end_node)
    
    # Store results
    evaluation_results = {
        "BFS": {
            "path_length": len(bfs_path),
            "execution_time": bfs_time
        },
        "DFS": {
            "path_length": len(dfs_path),
            "execution_time": dfs_time
        },
        "Dijkstra": {
            "path_length": len(dijkstra_path),
            "execution_time": dijkstra_time
        },
        "A*": {
            "path_length": len(a_star_path),
            "execution_time": a_star_time
        }
    }
    
    # Print evaluation summary
    print("\n📊 Resultados de evaluación (longitud del camino y tiempo de ejecución):")
    for algo, results in evaluation_results.items():
        print(f"{algo}: longitud del camino = {results['path_length']}, tiempo = {results['execution_time']:.6f} segundos")
    
    # Compare paths
    print("\n🔎 Comparación de longitud de caminos:")
    path_lengths = [result["path_length"] for result in evaluation_results.values() if result["path_length"] > 0]
    if path_lengths:
        shortest_path_length = min(path_lengths)
        for algo, result in evaluation_results.items():
            if result["path_length"] == shortest_path_length and result["path_length"] > 0:
                print(f"✅ {algo} encontró una de las rutas más cortas ({result['path_length']} pasos)")
    
    # Compare execution times
    print("\n⚡ Comparación de tiempos de ejecución:")
    fastest_time = min(result["execution_time"] for result in evaluation_results.values())
    for algo, result in evaluation_results.items():
        if result["execution_time"] == fastest_time:
            print(f"✅ {algo} fue el más rápido ({result['execution_time']:.6f} segundos)")
    
    # Visualize results
    visualize_results(maze, bfs_path, dfs_path, dijkstra_path, a_star_path, evaluation_results, maze_file)


def study_case_2():
    from P1_MazeLoader import MazeLoader
    print('-'*30,"\nThis is study case 2\n",'-'*30)
    maze_file = 'laberinto2.txt'
    maze = MazeLoader(maze_file).load_Maze().plot_maze()
    # Aquí la implementación de la solución:
    graph = maze.get_graph(visualize=True)
    
    # Get start and end positions from the maze
    start_node = maze.start
    end_node = maze.end
    print(f"Start: {start_node}, End: {end_node}")
    
    # Run all search algorithms
    print("\nEjecutando algoritmos de búsqueda...")
    bfs_path, bfs_time = bfs(graph, start_node, end_node)
    dfs_path, dfs_time = dfs(graph, start_node, end_node)
    dijkstra_path, dijkstra_time = dijkstra(graph, start_node, end_node)
    a_star_path, a_star_time = a_star(graph, start_node, end_node)
    
    # Store results
    evaluation_results = {
        "BFS": {
            "path_length": len(bfs_path),
            "execution_time": bfs_time
        },
        "DFS": {
            "path_length": len(dfs_path),
            "execution_time": dfs_time
        },
        "Dijkstra": {
            "path_length": len(dijkstra_path),
            "execution_time": dijkstra_time
        },
        "A*": {
            "path_length": len(a_star_path),
            "execution_time": a_star_time
        }
    }
    
    # Print evaluation summary
    print("\n📊 Resultados de evaluación (longitud del camino y tiempo de ejecución):")
    for algo, results in evaluation_results.items():
        print(f"{algo}: longitud del camino = {results['path_length']}, tiempo = {results['execution_time']:.6f} segundos")
    
    # Compare paths
    print("\n🔎 Comparación de longitud de caminos:")
    path_lengths = [result["path_length"] for result in evaluation_results.values() if result["path_length"] > 0]
    if path_lengths:
        shortest_path_length = min(path_lengths)
        for algo, result in evaluation_results.items():
            if result["path_length"] == shortest_path_length and result["path_length"] > 0:
                print(f"✅ {algo} encontró una de las rutas más cortas ({result['path_length']} pasos)")
    
    # Compare execution times
    print("\n⚡ Comparación de tiempos de ejecución:")
    fastest_time = min(result["execution_time"] for result in evaluation_results.values())
    for algo, result in evaluation_results.items():
        if result["execution_time"] == fastest_time:
            print(f"✅ {algo} fue el más rápido ({result['execution_time']:.6f} segundos)")
    
    # Visualize results
    visualize_results(maze, bfs_path, dfs_path, dijkstra_path, a_star_path, evaluation_results, maze_file)


def study_case_3():
    from P1_MazeLoader import MazeLoader
    print('-'*30,"\nThis is study case 3\n",'-'*30)
    maze_file = 'laberinto3.txt'
    maze = MazeLoader(maze_file).load_Maze().plot_maze()
    # Aquí la implementación de la solución:
    graph = maze.get_graph(visualize=True)
    
    # Get start and end positions from the maze
    start_node = maze.start
    end_node = maze.end
    print(f"Start: {start_node}, End: {end_node}")
    
    # Run all search algorithms
    print("\nEjecutando algoritmos de búsqueda...")
    bfs_path, bfs_time = bfs(graph, start_node, end_node)
    dfs_path, dfs_time = dfs(graph, start_node, end_node)
    dijkstra_path, dijkstra_time = dijkstra(graph, start_node, end_node)
    a_star_path, a_star_time = a_star(graph, start_node, end_node)
    
    # Store results
    evaluation_results = {
        "BFS": {
            "path_length": len(bfs_path),
            "execution_time": bfs_time
        },
        "DFS": {
            "path_length": len(dfs_path),
            "execution_time": dfs_time
        },
        "Dijkstra": {
            "path_length": len(dijkstra_path),
            "execution_time": dijkstra_time
        },
        "A*": {
            "path_length": len(a_star_path),
            "execution_time": a_star_time
        }
    }
    
    # Print evaluation summary
    print("\n📊 Resultados de evaluación (longitud del camino y tiempo de ejecución):")
    for algo, results in evaluation_results.items():
        print(f"{algo}: longitud del camino = {results['path_length']}, tiempo = {results['execution_time']:.6f} segundos")
    
    # Compare paths
    print("\n🔎 Comparación de longitud de caminos:")
    path_lengths = [result["path_length"] for result in evaluation_results.values() if result["path_length"] > 0]
    if path_lengths:
        shortest_path_length = min(path_lengths)
        for algo, result in evaluation_results.items():
            if result["path_length"] == shortest_path_length and result["path_length"] > 0:
                print(f"✅ {algo} encontró una de las rutas más cortas ({result['path_length']} pasos)")
    
    # Compare execution times
    print("\n⚡ Comparación de tiempos de ejecución:")
    fastest_time = min(result["execution_time"] for result in evaluation_results.values())
    for algo, result in evaluation_results.items():
        if result["execution_time"] == fastest_time:
            print(f"✅ {algo} fue el más rápido ({result['execution_time']:.6f} segundos)")
    
    # Visualize results
    visualize_results(maze, bfs_path, dfs_path, dijkstra_path, a_star_path, evaluation_results, maze_file)

if __name__ == '__main__':
    study_case_1()
    study_case_2()
    study_case_3()

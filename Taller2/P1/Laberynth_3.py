from Taller2.P1.P1_MazeLoader_3 import MazeLoader
import copy
import heapq

def load_laberynth():
    maze = MazeLoader('laberinto3.txt').load_Maze()
    graph_3 = maze.get_graph()
    return maze, graph_3

def nayfeth(maze):
    new_maze = copy.deepcopy(maze)
    height = len(new_maze.maze)
    width = len(new_maze.maze[0])

    # Posible directions
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Iterate through each cell in the maze and translate the result
    translate = {' ': 0, '#': 1}
    
    new_maze.maze = [[translate.get(x, x)for x in row] 
                     for row in new_maze.maze]
    
        
    for r in range(height):
        for c in range(width):
            cell = new_maze.maze[r][c]
            if cell == 1 or cell == 'E' or cell == 'S':
                continue
            wall_count = 0

            for dr, dc in directions:
                
                nr, nc = r + dr, c + dc
                
                if 0 <= nr < height and 0 <= nc < width \
                        and new_maze.maze[nr][nc] == 1:
                    wall_count += 1

            if wall_count == 3:
                new_maze.maze[r][c] = 1


        
    # Re translate maze
    translate = {0: ' ', 1: '#'}
    new_maze.maze = [[translate.get(x, x)for x in row] 
                     for row in new_maze.maze]
    
    
    return new_maze
    # function to find the path through a* algorithm 
def astar(maze):
    # find initial and final positions
    start = end = None
    for r in range(len(maze.maze)):
        for c in range(len(maze.maze[0])):
            if maze.maze[r][c] == 'S':
                start = (r, c)
            elif maze.maze[r][c] == 'E':
                end = (r, c)
    
    if not start or not end:
        raise ValueError('Start or end point not found.')
    
    def heuristic(a, b):
        
        h = abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        return h

    graph = maze.get_graph()
    # define initial state
    frontier = [(0 + heuristic(start, end), 0, start, [start])] # (f, g, current, path)
    # set to store visited nodes
    visited = set()

    # star looping
    while frontier:

        f, g, current, path = heapq.heappop(frontier)

        if current == end:
            solution_path = path
            return solution_path

        if current in visited:
            continue

        visited.add(current)

        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                g_new = g + 1
                f_new = g_new +heuristic(neighbor, end)
                heapq.heappush(frontier, (f_new, g_new, neighbor, path + [neighbor]))


maze, graph = load_laberynth()

solved_maze_nay = nayfeth(maze)

solved_maze_astar = astar(maze)

maze.plot_maze(path=solved_maze_astar, show_graph=True)

solved_maze_nay.plot_maze(show_graph=True)
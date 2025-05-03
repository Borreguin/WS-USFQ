from P1_MazeLoader import MazeLoader

def load_laberynth():
    maze = MazeLoader('laberinto3.txt').load_Maze().plot_maze()
    graph_3 = maze.get_graph()
    return maze
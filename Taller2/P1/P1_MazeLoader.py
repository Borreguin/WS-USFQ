import matplotlib.pyplot as plt
import os, sys
project_path = os.path.dirname(__file__)

parent_path = os.path.dirname(project_path)
sys.path.append(parent_path)
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
        plt.show()
        return self

    def get_graph(self, visualize=False):
        """Create a graph representation of the maze
        
        Args:
            visualize (bool): Whether to display a visualization of the graph
        
        Returns:
            dict: The graph representation of the maze
        """
        height = len(self.maze)
        width = len(self.maze[0])
        graph = {}
        
        # Find start and end positions
        self.start = None
        self.end = None
        for y in range(height):
            for x in range(width):
                if self.maze[y][x] == 'S':
                    self.start = (y, x)
                elif self.maze[y][x] == 'E':
                    self.end = (y, x)
        
        # Define the four possible movement directions (up, right, down, left)
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        # Build the graph
        for y in range(height):
            for x in range(width):
                # Skip walls
                if self.maze[y][x] == '#':
                    continue
                    
                # Create node for this position
                node = (y, x)
                graph[node] = []
                
                # Check all four neighbors
                for dy, dx in directions:
                    ny, nx = y + dy, x + dx
                    
                    # Check if neighbor is within bounds and not a wall
                    if (0 <= ny < height and 0 <= nx < width and 
                        self.maze[ny][nx] != '#'):
                        graph[node].append((ny, nx))
        
        # Visualize the graph if requested
        if visualize:
            self._visualize_graph(graph)
        
        return graph

    def _visualize_graph(self, graph):
        """Visualize the maze as a graph with nodes and edges"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Draw the maze as background
        height = len(self.maze)
        width = len(self.maze[0])
        for y in range(height):
            for x in range(width):
                cell = self.maze[y][x]
                color = define_color(cell)
                alpha = 0.3  # Semi-transparent to see the graph overlay
                ax.fill([x, x+1, x+1, x], [y, y, y+1, y+1], color=color, alpha=alpha, edgecolor='black')
        
        # Draw nodes
        for node in graph:
            y, x = node
            if node == self.start:
                color = 'green'
                size = 100
                label = 'Start'
            elif node == self.end:
                color = 'red'
                size = 100
                label = 'End'
            else:
                color = 'blue'
                size = 30
                label = None
            ax.scatter(x + 0.5, y + 0.5, color=color, s=size, zorder=10, label=label)
        
        # Draw edges
        for node, neighbors in graph.items():
            y, x = node
            for neighbor in neighbors:
                ny, nx = neighbor
                ax.plot([x + 0.5, nx + 0.5], [y + 0.5, ny + 0.5], 'k-', alpha=0.6, zorder=5)
        
        # Set the limits and invert y-axis
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        ax.invert_yaxis()
        
        # Remove ticks
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Create a legend (only for start and end nodes)
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='upper right')
        
        # Set title
        ax.set_title("Graph Representation of the Maze")
        
        plt.tight_layout()
        plt.show()

    def plot_paths(self, paths_dict, ax=None):
        """Plot the maze with multiple paths overlaid"""
        height = len(self.maze)
        width = len(self.maze[0])
        
        if ax is None:
            fig, ax = plt.subplots(figsize=(width/4, height/4))
        
        # Plot the maze
        for y in range(height):
            for x in range(width):
                cell = self.maze[y][x]
                color = define_color(cell)
                ax.fill([x, x+1, x+1, x], [y, y, y+1, y+1], color=color, edgecolor='black')
        
        # Plot each path with a different color/style
        colors = ['blue', 'orange', 'purple', 'green']
        styles = ['-', '--', ':', '-.']
        
        for i, (algo_name, path) in enumerate(paths_dict.items()):
            if path and len(path) > 0:
                # Get coordinates
                y_coords = [p[0] + 0.5 for p in path] 
                x_coords = [p[1] + 0.5 for p in path] 
                # Plot the path
                color_idx = i % len(colors)
                style_idx = i % len(styles)
                ax.plot(x_coords, y_coords, color=colors[color_idx], 
                    linestyle=styles[style_idx], label=algo_name)
        
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        ax.invert_yaxis()  # Invert y-axis to match maze coordinates
        ax.set_xticks([])
        ax.set_yticks([])
        ax.legend()
        
        return ax

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class AntColonyOptimization:
    def __init__(self, start, end, obstacles, grid_size=(10, 10), num_ants=10, evaporation_rate=0.1, alpha=0.1, beta=15):
        self.start = start
        self.end = end
        self.obstacles = obstacles
        self.grid_size = grid_size
        self.num_ants = num_ants
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta # alpha y beta ajustan el peso de las feromonas y la heurística.
        self.pheromones = np.ones(grid_size)
        self.best_path = None

    def _get_neighbors(self, position):
        pos_x, pos_y = position
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_x, new_y = pos_x + i, pos_y + j
                if (0 <= new_x < self.grid_size[0] and
                    0 <= new_y < self.grid_size[1] and
                    (new_x, new_y) != position and
                    (new_x, new_y) not in self.obstacles):
                    # Penalizar vecinos con muchos obstáculos alrededor
                    num_obstacles = sum((nx, ny) in self.obstacles for nx in range(new_x - 1, new_x + 2) for ny in
                                        range(new_y - 1, new_y + 2))
                    if num_obstacles < 3:  # Evitar zonas muy bloqueadas
                        neighbors.append((new_x, new_y))
        return neighbors

    def _select_next_position(self, position, visited):
        neighbors = self._get_neighbors(position)
        probabilities = []
        total = 0
        for neighbor in neighbors:
            if neighbor not in visited:
                pheromone = self.pheromones[neighbor[1], neighbor[0]]
                heuristic = 1 / (np.linalg.norm(np.array(neighbor) - np.array(self.end)) + 0.1)
                score = pheromone ** self.alpha * heuristic ** self.beta
                probabilities.append((neighbor, score))
                total += score
        if not probabilities:
            return None
        probabilities = [(pos, prob / total) for pos, prob in probabilities]
        selected = np.random.choice(len(probabilities), p=[prob for pos, prob in probabilities])
        return probabilities[selected][0]

    def _evaporate_pheromones(self):
        self.pheromones *= (1 - self.evaporation_rate)

    def _deposit_pheromones(self, path):
        for position in path:
            self.pheromones[position[1], position[0]] += 1
    """

    def _deposit_pheromones(self, path):
        if len(path) > 1:  # Evitar división por cero
            distancia_total = self.calcular_distancia_total(path)  # Usar la función existente
            feromona_value = 1 / distancia_total  # Cuanto menor sea la distancia, mayor depósito

            for position in path:
                self.pheromones[position[1], position[0]] += feromona_value  # Aplicar refuerzo proporcional
    """
    @staticmethod
    def calcular_distancia_total(camino):
        distancia_total = 0
        for i in range(len(camino) - 1):
            distancia_total += np.linalg.norm(np.array(camino[i]) - np.array(camino[i + 1]))
        return distancia_total

    def find_best_path(self, num_iterations):
        for _ in range(num_iterations):
            all_paths = []
            for _ in range(self.num_ants):
                current_position = self.start
                path = [current_position]
                """
                while current_position != self.end:
                    next_position = self._select_next_position(current_position, path)
                    if next_position is None:
                        break
                    path.append(next_position)
                    current_position = next_position
<<<<<<< HEAD

                if current_position == self.end:
                    all_paths.append(path)

            if not all_paths:
                continue

            all_paths.sort(key=lambda x: len(x))
=======
                
                """
                while current_position != self.end:
                    next_position = self._select_next_position(current_position, path)
                    if next_position is None:
                        # Reiniciar hormiga si queda atrapada
                        current_position = self.start
                        path = [current_position]
                        continue
                    path.append(next_position)
                    current_position = next_position
                all_paths.append(path)
            # Escoger el mejor camino por su tamaño?
            # --------------------------
            #all_paths.sort(key=lambda x: len(x))
            #best_path = all_paths[0]
            all_paths.sort(key=lambda r: self.calcular_distancia_total(r))
>>>>>>> origin/Grupo-5
            best_path = all_paths[0]

            self._evaporate_pheromones()
            self._deposit_pheromones(best_path)

            if self.best_path is None or len(best_path) < len(self.best_path):
                self.best_path = best_path

    def plot(self, save_as=None):
        cmap = LinearSegmentedColormap.from_list('pheromone', ['white', 'green', 'red'])
        plt.figure(figsize=(8, 8))
        plt.imshow(self.pheromones, cmap=cmap, vmin=np.min(self.pheromones), vmax=np.max(self.pheromones))
        plt.colorbar(label='Pheromone intensity')
        plt.scatter(self.start[0], self.start[1], color='orange', label='Start', s=100)
        plt.scatter(self.end[0], self.end[1], color='magenta', label='End', s=100)
        for obstacle in self.obstacles:
            plt.scatter(obstacle[0], obstacle[1], color='gray', s=900, marker='s')
        if self.best_path:
            path_x, path_y = zip(*self.best_path)
            plt.plot(path_x, path_y, color='blue', label='Best Path', linewidth=3)
        plt.xlabel('Column')
        plt.ylabel('Row')
        plt.title('Ant Colony Optimization')
        plt.legend()
        plt.grid(True)
        if save_as:
            plt.savefig(save_as, dpi=150)
            print(f"Imagen guardada como {save_as}")
        else:
            plt.show()

def study_case_1():
    print("Start of Ant Colony Optimization - First Study Case")
    start = (0, 0)
    end = (4, 7)
    obstacles = [(1, 2), (2, 2), (3, 2)]
    aco = AntColonyOptimization(start, end, obstacles)
    aco.find_best_path(100)
    aco.plot(save_as="aco_case1.png")
    print("End of Ant Colony Optimization")
    print("Best path:", aco.best_path)

def study_case_2():
    print("Start of Ant Colony Optimization - Second Study Case")
    start = (0, 0)
    end = (4, 7)
    obstacles = [(0, 2), (1, 2), (2, 2), (3, 2)]
    aco = AntColonyOptimization(
        start, end, obstacles,
        num_ants=30,
        evaporation_rate=0.05,
        alpha=1.0,
        beta=10
    )
    aco.find_best_path(100)
    aco.plot(save_as="aco_case2.png")
    print("End of Ant Colony Optimization")
    print("Best path:", aco.best_path)

if __name__ == '__main__':
    print('\ncaso de estudio 1')
    study_case_1()
<<<<<<< HEAD
    # study_case_2()
=======
    print('\ncaso de estudio 2')
    study_case_2()



>>>>>>> origin/Grupo-5

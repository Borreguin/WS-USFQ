#Resolucion del problema de la torre de Hanoi - Carla Parra
import heapq
import matplotlib.pyplot as plt

# Algoritmo A* para Torre de Hanoi
def hanoi_a_star(n):
    start = (tuple(range(n, 0, -1)), (), ())
    goal = ((), (), tuple(range(n, 0, -1)))

    frontier = []
    heapq.heappush(frontier, (heuristic(start, n), 0, start, []))

    visited = set()
    expansion_steps = []

    while frontier:
        estimated_total_cost, cost_so_far, current, path = heapq.heappop(frontier)

        if current == goal:
            return path + [current], expansion_steps

        if current in visited:
            continue

        visited.add(current)

        for next_state, move in neighbors(current):
            if next_state not in visited:
                new_cost = cost_so_far + 1
                estimated_cost = new_cost + heuristic(next_state, n)
                heapq.heappush(frontier, (estimated_cost, new_cost, next_state, path + [current]))
                expansion_steps.append(len(visited))

    return None, None

def heuristic(state, n):
    return n - len(state[2])

def neighbors(state):
    result = []
    for i in range(3):
        if not state[i]:
            continue
        disk = state[i][-1]
        for j in range(3):
            if i == j:
                continue
            if not state[j] or state[j][-1] > disk:
                new_state = list(map(list, state))
                new_state[i] = new_state[i][:-1]
                new_state[j] = new_state[j] + [disk]
                result.append((tuple(map(tuple, new_state)), (i, j)))
    return result

def graficar_expansiones(expansiones):
    plt.figure(figsize=(10,6))
    plt.plot(range(1, len(expansiones)+1), expansiones, marker='o', color='skyblue')
    plt.title("Expansiones de nodos en A* para Torre de Hanoi")
    plt.xlabel("Iteraciones")
    plt.ylabel("Nodos Expandidos")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    n_discos = 3  # Puedes probar con 3 o 4 discos
    solucion, expansiones = hanoi_a_star(n_discos)

    if solucion:
        print(f"\nSolución encontrada en {len(solucion) - 1} movimientos!")
        graficar_expansiones(expansiones)
    else:
        print("No se encontró solución.")


import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation

# Grafo global
G = nx.DiGraph()
frames = []
last_nodes = []
all_states = []
initial_state = None
final_state = None

# Agregar estado
def agregar_estado(torres, iteracion_actual):
    estado = tuple(map(tuple, torres))
    G.add_node(estado, subset=iteracion_actual, label=str(estado))
    all_states.append((iteracion_actual, estado))
    return estado

# Mover y construir grafo
def mover_hanoi_grafo(n, origen, destino, auxiliar, torres, n_discos, iteracion_actual, padre=None):
    global final_state
    if n == 1:
        disco = torres[origen].pop()
        torres[destino].append(disco)
        nuevo_estado = agregar_estado(torres, iteracion_actual + 1)
        if padre is not None:
            G.add_edge(padre, nuevo_estado)
            frames.append(list(G.edges))
            last_nodes.append(nuevo_estado)
        final_state = nuevo_estado
        return iteracion_actual + 1, nuevo_estado
    else:
        iteracion_actual, nuevo_padre = mover_hanoi_grafo(n-1, origen, auxiliar, destino, torres, n_discos, iteracion_actual, padre)
        iteracion_actual, nuevo_padre = mover_hanoi_grafo(1, origen, destino, auxiliar, torres, n_discos, iteracion_actual, nuevo_padre)
        iteracion_actual, nuevo_padre = mover_hanoi_grafo(n-1, auxiliar, destino, origen, torres, n_discos, iteracion_actual, nuevo_padre)
        return iteracion_actual, nuevo_padre

# Configuracion inicial
n_discos = 3

# Torres iniciales
torres = [list(reversed(range(1, n_discos+1))), [], []]

# Inicializar grafo
initial_state = agregar_estado(torres, 0)

# Construir grafo
mover_hanoi_grafo(n_discos, 0, 2, 1, torres, n_discos, 0, initial_state)

# Layout fijo para la animacion
pos = nx.spring_layout(G, seed=42)

# Crear figura
fig, ax = plt.subplots(figsize=(14, 10))

# Función de actualizacion de frames
def update(num):
    ax.clear()
    ax.set_title("Construcción del Grafo de Estados de Torre de Hanoi", fontsize=16)
    edges_to_draw = frames[num]
    subG = nx.DiGraph()
    subG.add_edges_from(edges_to_draw)
    subG.add_nodes_from(G.nodes(data=True))

    node_colors = []
    for n in subG.nodes:
        if n == last_nodes[num]:
            node_colors.append('red')  # Nodo recientemente agregado
        else:
            node_colors.append(plt.cm.plasma(G.nodes[n]['subset'] / (n_discos*2)))

    nx.draw(subG, pos, with_labels=False, node_color=node_colors, node_size=800, arrowsize=20, ax=ax)
    labels = {n: G.nodes[n]['label'] for n in subG.nodes}
    nx.draw_networkx_labels(subG, pos, labels=labels, font_size=7, font_color='white', ax=ax)

# Crear animacion
ani = animation.FuncAnimation(fig, update, frames=len(frames), interval=1000, repeat=False)

# Guardar animacion como GIF
ani.save("hanoi_graph_animation.gif", writer='pillow')

# Mostrar estado inicial, estados intermedios y estado final
print("Estado inicial:")
print(initial_state)
print("\nEstados intermedios:")
for i, estado in all_states[1:-1]:
    print(f"Iteracion {i}: {estado}")
print("\nEstado final (solución):")
print(final_state)
print(f"\nNumero total de estados para llegar a la solución: {len(G.nodes)}")

# Graficar todo el grafo final
graph_fig, graph_ax = plt.subplots(figsize=(14, 10))
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=800, arrowsize=20, ax=graph_ax)
labels = {n: G.nodes[n]['label'] for n in G.nodes}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, font_color='black', ax=graph_ax)
plt.title("Grafo Completo de Estados de Torre de Hanoi", fontsize=16)
plt.show()

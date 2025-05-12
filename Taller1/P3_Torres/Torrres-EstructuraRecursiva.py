#Carla Parra, resolución de problema de Torre de Hanoi.
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import imageio

# Lista para almacenar los fotogramas del GIF
frames = []
iteracion = 0  # Contador global de movimientos

# Paleta de colores para los discos
colores = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6']

def dibujar_torres(torres, n_discos, iteracion_actual):
    """Dibuja las torres, los discos y las etiquetas para un estado específico"""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_facecolor('#1e1e1e')  # Fondo oscuro
    ax.set_xlim(0, 9)
    ax.set_ylim(0, n_discos + 6)
    ax.axis('off')  # Oculta ejes

    postes_x = [1.5, 4.5, 7.5]  # Coordenadas X de los postes
    nombres_postes = ['Origen', 'Auxiliar', 'Destino']  # Etiquetas

    # Dibujar los postes verticales
    for idx, base in enumerate(postes_x):
        ax.plot([base, base], [0, n_discos + 1], color='white', linewidth=4)
        ax.text(base, 0.3, nombres_postes[idx], ha='center', va='bottom', color='white', fontsize=13, weight='bold')

    # Dibujar la base horizontal de las torres
    ax.plot([0.5, 8.5], [0, 0], color='gray', linewidth=5)

    # Dibujar los discos en cada torre
    for i, torre in enumerate(torres):
        x_base = postes_x[i]
        for j, disco in enumerate(torre):
            ancho = disco * 0.6 + 0.4  # Determina el ancho del disco
            color = colores[(disco - 1) % len(colores)]
            rect = patches.Rectangle(
                (x_base - ancho/2, j + 1),
                ancho,
                0.6,
                linewidth=1,
                edgecolor='white',
                facecolor=color
            )
            ax.add_patch(rect)
            ax.text(x_base, j + 1.3, str(disco), ha='center', va='center', fontsize=9, color='white', weight='bold')

    # Mostrar la iteración actual en la parte superior
    ax.text(4.5, n_discos + 5, f"Iteración: {iteracion_actual}", ha='center', va='top', fontsize=16, color='cyan', weight='bold')

    # Captura el frame del canvas y lo agrega a la lista
    fig.canvas.draw()
    frame = np.asarray(fig.canvas.buffer_rgba())[:, :, :3]
    frames.append(frame)
    plt.close()

def mover_hanoi(n, origen, destino, auxiliar, torres, n_discos):
    """Algoritmo recursivo que resuelve la Torre de Hanoi"""
    global iteracion
    if n == 1:
        # Mover un solo disco directamente
        disco = torres[origen].pop()
        torres[destino].append(disco)
        iteracion += 1
        dibujar_torres(torres, n_discos, iteracion)
    else:
        # Paso 1: Mover n-1 discos al auxiliar
        mover_hanoi(n-1, origen, auxiliar, destino, torres, n_discos)
        # Paso 2: Mover el disco más grande al destino
        mover_hanoi(1, origen, destino, auxiliar, torres, n_discos)
        # Paso 3: Mover n-1 discos desde auxiliar a destino
        mover_hanoi(n-1, auxiliar, destino, origen, torres, n_discos)

# Configuración inicial de las torres
n_discos = 5
torres = [list(reversed(range(1, n_discos+1))), [], []]  # Torre A con todos los discos

# Inicialización de la animación
iteracion = 0
dibujar_torres(torres, n_discos, iteracion)
mover_hanoi(n_discos, 0, 2, 1, torres, n_discos)

# Guardar el GIF animado
fps = 2  # Velocidad del GIF
imageio.mimsave("torre_hanoi_etiquetas_iteraciones.gif", frames, fps=fps)
print("GIF generado exitosamente como 'torre_hanoi_etiquetas_iteraciones.gif'")

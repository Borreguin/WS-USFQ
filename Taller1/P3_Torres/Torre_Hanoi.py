import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configuración
n_disks = 3
torres_iniciales = {'A': list(range(n_disks, 0, -1)), 'B': [], 'C': []}
estados = []

def guardar_estado(torres):
    estado_copia = {k: v.copy() for k, v in torres.items()}
    estados.append(estado_copia)

def torre_de_hanoi(n, origen, destino, auxiliar, torres):
    if n == 1:
        disco = torres[origen].pop()
        torres[destino].append(disco)
        guardar_estado(torres)
    else:
        torre_de_hanoi(n - 1, origen, auxiliar, destino, torres)
        torre_de_hanoi(1, origen, destino, auxiliar, torres)
        torre_de_hanoi(n - 1, auxiliar, destino, origen, torres)

def dibujar_todos_estados(estados):
    total_pasos = len(estados)
    columnas = 4
    filas = (total_pasos + columnas - 1) // columnas

    fig, axes = plt.subplots(filas, columnas, figsize=(4 * columnas, 3 * filas))
    axes = axes.flatten()

    posiciones = {'A': 1.5, 'B': 4.5, 'C': 7.5}

    for idx, estado in enumerate(estados):
        ax = axes[idx]
        ax.set_xlim(0, 9)
        ax.set_ylim(0, n_disks + 2)
        ax.set_xticks([1.5, 4.5, 7.5])
        ax.set_xticklabels(['A', 'B', 'C'])
        ax.set_yticks([])
        ax.set_title(f'Paso {idx + 1}')

        # Dibujar fondo/borde divisorio al final del subplot
        ax.axvline(x=9, color='lightgray', linewidth=2)

        for x in posiciones.values():
            ax.add_patch(patches.Rectangle((x - 0.2, 0), 0.4, 0.1, color='black'))
            ax.add_patch(patches.Rectangle((x - 0.05, 0), 0.1, n_disks + 1, color='gray', alpha=0.5))

        for torre, discos in estado.items():
            for nivel, disco in enumerate(discos):
                ancho = disco * 0.3
                x = posiciones[torre]
                y = nivel + 1
                ax.add_patch(patches.Rectangle((x - ancho / 2, y), ancho, 0.4, color='blue'))
                ax.text(x, y + 0.1, str(disco), ha='center', va='center', color='white', fontsize=8)
        ax.axis('off')

    for j in range(len(estados), len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()

# Ejecutar
guardar_estado(torres_iniciales)
torres = {k: v.copy() for k, v in torres_iniciales.items()}
torre_de_hanoi(n_disks, 'A', 'C', 'B', torres)
dibujar_todos_estados(estados)




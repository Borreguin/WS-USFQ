import matplotlib.pyplot as plt
import time


def graficar_torres(torres):
    plt.clf()
    colores = ['red', 'green', 'blue']
    for i, torre in enumerate(torres):
        for j, disco in enumerate((torre)):
            plt.bar(i * 2, disco, bottom=j, width=1.5,
                    color=colores[disco - 1])
            # Mostrar el número del disco
            plt.text(i * 2, j + 0.2, str(disco), ha='center',
                     va='bottom', fontsize=12, color='white')
    plt.xticks([0, 2, 4], ['A', 'B', 'C'])
    plt.title("Torre de Hanoi")
    plt.ylim(0, 6)
    plt.pause(2)

# Check de movimientos de disco


def mover_disco(torres, origen, destino):
    if not torres[origen]:
        raise ValueError(
            f"No se puede mover desde la torre {origen}, está vacía.")
    disco = torres[origen][-1]
    if torres[destino] and torres[destino][-1] < disco:
        raise ValueError(
            f"No se puede colocar el disco {disco} sobre uno más pequeño ({torres[destino][-1]}).")

    torres[origen].pop()
    torres[destino].append(disco)
    graficar_torres(torres)

# Lógica recursiva de Hanoi


def hanoi(n, origen, destino, auxiliar, torres):
    if n == 1:
        mover_disco(torres, origen, destino)
    else:
        hanoi(n - 1, origen, auxiliar, destino, torres)
        mover_disco(torres, origen, destino)
        hanoi(n - 1, auxiliar, destino, origen, torres)


n_discos = 3
torres = [list(reversed(range(1, n_discos + 1))), [], []]  # A, B, C

plt.figure(figsize=(6, 6))
graficar_torres(torres)


hanoi(n_discos, 0, 2, 1, torres)

plt.show()

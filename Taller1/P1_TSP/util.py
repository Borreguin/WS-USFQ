import random
import string
import math
import matplotlib.pyplot as plt

def generar_ciudades(n_cities: int, seed: int = 123):
    random.seed(seed)
    cities = {}
    for i in range(n_cities):
        ciudad = f"{random.choice(string.ascii_uppercase)}{random.randint(0,9)}"
        x = round(random.uniform(-100, 100), 1)
        y = round(random.uniform(-100, 100), 1)
        cities[ciudad] = (x, y)
    return cities

def calcular_distancia(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def generar_distancias(ciudades):
    distancias = {}
    for ciudad1, coord1 in ciudades.items():
        for ciudad2, coord2 in ciudades.items():
            if ciudad1 != ciudad2:
                distancias[(ciudad1, ciudad2)] = round(calcular_distancia(coord1, coord2), 2)
    return distancias

def generar_ciudades_con_distancias(n_cities: int):
    ciudades = generar_ciudades(n_cities)
    distancias = generar_distancias(ciudades)
    return ciudades, distancias

def plotear_ruta(ciudades, ruta, mostrar_anotaciones=True):
    print("Ciudades:", list(ciudades.keys()))
    print("Ruta:", ruta)
    if not ruta:
        print("La ruta está vacía. No se puede plotear el resultado.")
        return
    #if isinstance(ruta[0], int):
     #   print("Convirtiendo índices a nombres de ciudades...")
      #  lista_nombres = list(ciudades.keys())
       # ruta = [lista_nombres[i] for i in ruta]
        #print("Ruta corregida:", ruta)

    coordenadas_x = [ciudades[ciudad][0] for ciudad in ruta]
    coordenadas_y = [ciudades[ciudad][1] for ciudad in ruta]

    coordenadas_x.append(coordenadas_x[0])
    coordenadas_y.append(coordenadas_y[0])

    plt.figure(figsize=(8, 6))
    plt.plot(coordenadas_x, coordenadas_y, 'ro-', label='Ruta')

    if mostrar_anotaciones:
        for ciudad, (x, y) in ciudades.items():
            plt.text(x, y, ciudad, fontsize=8, ha='right')

    plt.title('Ruta más corta encontrada')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.grid(True)
    plt.legend()
    plt.show()



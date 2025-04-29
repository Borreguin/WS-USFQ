## Taller 2 de inteligencia artificial

- **Grupo 1**
- **Integrantes del grupo**:
  * Patricia Lema
  * Ana Navas
  * Diana Córdova
  * Sebastián Ruiz

## 1. Uso de Algoritmos de Búsqueda

El objetivo de esta tarea es utilizar cualquier algoritmo de búsqueda para resolver los 3 laberintos propuestos, 
el reto es poder visualizar/representar los resultados, adicionalmente poder comparar al menos 2 algoritmos de búsqueda 
y mirar cómo se comportan para cada laberinto

### A. Leer el laberinto y representarlo como un grafo.

### B. Aplicar algoritmos de búsqueda

## 2. Optimización de Colonia de Hormigas

Ant	 Colony	 Optimization	 (ACO)	 es una técnica de optimización inspirada en el
comportamiento de las hormigas reales cuando buscan recursos para su colonia. El propósito
de este algoritmo en el campo de la IA es el de simular el comportamiento de las hormigas
para encontrar el mejor camino desde el nido de la colonia a la fuente de recursos.

### A. Correr la implementación planteada. Analizar el código.

Se corrió el programa para el caso de estudio 1 algunas veces. Para algunos de los casos, el camino seleccionado por el algoritmo no llegaba a la meta planteada. Al revisar el código, se observó que en el fragmento del código que hace que la hormiga recorra, cuando la posición siguiente no es válida, el algoritmo termina el trayecto actual, pero a pesar de no haber llegado a la meta lo almacena. Posteriormente, de todos los caminos almacenados, el algoritmo selecciona el más corto, lo que quiere decir que a pesar de haber fallado en el trayecto, si un camino erróneo es más corto que cualquier camino correcto, el algoritmo seleccionará y graficará el camino más corto.

Para resolver esto, se añadió un paso entre el recorrido de todas las hormigas, y la selección del mejor camino. A fin de comparar solamente caminos que llegan a la meta, se creo una lista `valid_paths` que es poblada por los caminos en `all_paths` que han alcanzado la meta.

### B. Que ocurre con el 2do caso de estudio?

En el 2do caso de estudio se hubiesen visto fallas en todas las iteraciones, pero se realizó la corrección detallada en el literal A antes de empezar con el 2do caso.

Sin embargo, se observó una pecularidad en los caminos que se graficaban en el 2do caso: una vez superados los obstáculos, a pesar de tener un camino recto hacia la meta, el camino seleccionado era uno en el cual había una desviación de 45º que era corregida en el siguiente paso. Esto se debe a la naturaleza estocástica del modelo, una vez que las hormigas empiezan a caminar por este tipo de caminos, el camino es reforzado debido a la forman en la que el parámetro de las feromonas influye en la caminata de hormigas subsecuentes.

Con el fin de solucionar esto, se puede incrementar el valor del parámetro `beta` del modelo, el cual controla la influencia de la distancia. Para valores altos de `beta`, hay una atracción mayor hacia la meta.

### C. Describir los parámetros del modelo.

* start: Las coordinadas posición inicial de las hormigas.
* end: Las coordinadas de la ubicación de la meta.
* obstacles: Lista que contiene las coordenadas sobre las cuales las hormigas no pueden moverse.
* grid_size: El tamaño de la cuadrícula (10x10 en este caso)
* num_ants: El número de hormigas que actúan en cada iteración.
* evaporation_rate: un parámetro que define la tasa con la que se disipan las feromonas.
* alpha: el peso del rastro de feromonas en el camino que toman las hormigas subsecuentes.
* beta: el peso que regula la atracción de las hormigas hacia la meta.

### D. Pregunta de investigación: será que se puede utilizar este algoritmo para resolver el TSP Cuales serían sus pasos de implementación?

